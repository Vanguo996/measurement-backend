import grpc
import logging
import pyvisa as visa
from pyvisa.resources.gpib import GPIBInstrument
from pyvisa.resources.resource import Resource
from sweep_pb2 import response
import sweep_pb2_grpc as pb2_grpc

from concurrent.futures import ThreadPoolExecutor
import config
from sweep import SweepTest

class InstrumentsServer(pb2_grpc.InstrumentsControllerServicer):

    def __init__(self):
        self.rm = visa.ResourceManager(config.visa_lib)
        logging.info("Resource Manager found in : {0}".format(config.visa_lib))


    def CloseOutput(self, request, context):
        instr_name = request.instruments_name
        instr = self.rm.open_resource(instr_name)
        res_name = instr.resource_name
        instr.write(":outp off")
        
        instr.close()

        closed_info = f"{res_name} OUTPUT CLOSED"
        logging.info(closed_info)
        return response(result=closed_info)

    def IVSweepMode(self, sweep_request, context):
        """返回stream数据流
        """
        start_volt = sweep_request.start_volt
        end_volt = sweep_request.end_volt
        volt_step = sweep_request.volt_step
        current_cmpl = sweep_request.current_cmpl
        mes_speed = sweep_request.mes_speed


        instr2400 = self.rm.open_resource(config.instr_2400)
        logging.info("opend resource：%s", config.instr_2400)

        self.sweep_config(instr2400, current_cmpl, mes_speed)

        source_volt_level = start_volt
        while 1:
            instr2400.write(':sour:volt:lev %s' % (source_volt_level))
            measure_i_info = instr2400.query(':read?') 
            logging.info(measure_i_info)
            yield response(result=measure_i_info)

            source_volt_level += volt_step
            source_volt_level = round(source_volt_level, 10)
            
            if source_volt_level > end_volt:
                break
        instr2400.write(":outp off")
        count, queue = self.get_errors(instr2400)
        logging.info(f"TOTAL ERRORS: {count} || {queue}")
        return response(result=f"TOTAL ERRORS: {count} || {queue}")


    def sweep_config(self, instr:Resource, current_cmpl, mes_speed):
        """
        """
        self.instr_init(instr)
        instr.write(":sour:func volt")
        instr.write(':sens:curr:prot %s' % current_cmpl)
        instr.write(':sens:func "curr:dc"')
        instr.write(':sens:curr:nplc %d' % mes_speed)
        
        instr.write(':trig:coun 5')
        instr.write(':trig:del 0')
        instr.write(':sour:del 0')
        instr.write(':outp on')


    def get_errors(self, instr: Resource):
        """get errors counts and errors queue
        """
        error_count = instr.query(':syst:err:coun?')
        # return and clear all errors
        error_queue = instr.query(':syst:err:all?')
        
        return error_count, error_queue


    def instr_init(self, instr: Resource):
        """初始化2400

        """
        instr.write("*rst?")
        
        # 关闭蜂鸣器
        instr.write(":syst:beep:stat off")
        logging.info("BEEPER CLOSED")

        # 关闭前面板
        # self.instr2400.write(":display:enable off")
        # logging.info("关闭前面板")

        # 重置时间戳
        instr.write(":syst:time:res")
        timestamp = instr.query(":syst:time?")
        logging.info("TIMESTAMP RESETD: %s", timestamp)

        
    def test_resource(self):
        """
        """
        test_instr = self.st.rm.open_resource(config.test_instr_name)
        inter_num = test_instr.interface_number
        res_name = test_instr.resource_name
        res_manu = test_instr.resource_manufacturer_name
        for i in range(100):
            logging.info(f"{i}, {test_instr}")
            # time
            # yield response(result=f"interface: {inter_num}, resource_name: {res_name}")

        
    # def mes-simulator(self):
    #     """
    #     ""
    #     i = 9999
    #     value1 = 100
    #     value2 = 50
    #     t = 0
    #     while i:
    #         value1 += randint(0, 10)
    #         value2 += randint(0, 10)

    #         data = '{},{},{}\n'.format(t, value1, value2)
    #         i -= 1
    #         t += 1
    #         time.sleep(1)
    #         logging.info(data)
    #         yield response(result=data)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    port = 52001
    grpc_server = grpc.server(ThreadPoolExecutor())
    
    pb2_grpc.add_InstrumentsControllerServicer_to_server(InstrumentsServer(), grpc_server)

    grpc_server.add_insecure_port(f"[::]:{port}")
    grpc_server.start()
    logging.info("server ready on port {0}".format(port))

    grpc_server.wait_for_termination()
    