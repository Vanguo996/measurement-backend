
import pyvisa as visa
import time
import logging

from . import config

class ConnectionTest():

    def __init__(self):
        self.rm = visa.ResourceManager(config.visa_lib)
        logging.info("资源管理器初始化完成")


    @staticmethod
    def connection_test(self, resource_name):
        """传入资源名称
        """
        instr = self.rm.open_resource(resource_name)
        return instr


    def list_all_instruments(self):
        """例如出所有仪器名称
        """
        list_of_instrs = self.rm.list_resources()
        logging.info("所有仪器:")
        


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt = '%Y-%m-%d  %H:%M:%S %a'    #注意月份和天数不要搞乱了，这里的格式化符与time模块相同
                    )

    ct = ConnectionTest()
    while 1:
        ct.list_all_instruments()
        instr = ct.connection_test(config.test_instr_name)
        print(instr)
        time.sleep(1)
        