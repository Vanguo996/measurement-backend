package main

import (
	"context"
	"log"

	pb "measurement-backend/pb"

	"google.golang.org/grpc"
)

const (
	instr2400  = "visa://202.197.78.43/GPIB0::24::INSTR"
	hostAddr   = "127.0.0.1:52001"
	dockerAddr = "127.0.0.1:52001"
)

// 关闭指定仪器的输入
func CloseOutputInstruments(client pb.InstrumentsControllerClient, resourceName string) {

	req_close_outp := &pb.Request{InstrumentsName: resourceName}

	response, err := client.CloseOutput(context.Background(), req_close_outp)
	if err != nil {
		log.Fatal(err)
	}

	log.Println(response.Result)
}

// 执行扫描任务
func SweepModeStart(client pb.InstrumentsControllerClient,
	StartVolt, VoltStep, EndVolt, CurrentCmpl, MesSpeed float32) {

	req := &pb.SweepRequest{
		StartVolt:   StartVolt,
		VoltStep:    VoltStep,
		EndVolt:     EndVolt,
		CurrentCmpl: CurrentCmpl,
		MesSpeed:    MesSpeed,
	}

	res, err := client.IVSweepMode(context.Background(), req)
	if err != nil {
		log.Fatal(err)
	}
	for {
		word, err := res.Recv()
		if err != nil {
			log.Fatal(err)
			break
		}

		log.Println(word)
		// time.Sleep(10 * time.Millisecond)
	}
	log.Println(res.Recv())
}

func main() {
	addr := hostAddr
	// addr := "172.17.0.3:52002"
	// conn, err := grpc.Dial(addr, grpc.WithInsecure(), grpc.WithBlock())
	conn, err := grpc.Dial(addr, grpc.WithInsecure())
	if err != nil {
		log.Fatal(err)
	}

	defer conn.Close()

	client := pb.NewInstrumentsControllerClient(conn)

	// CloseOutputInstruments(client, instr2400)

	SweepModeStart(client, -2, 0.1, 2, 100e-3, 1)

}
