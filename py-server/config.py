# coding=utf-8


ip_addr_local = "192.168.1.108"

ip_addr = "202.197.78.43"

visa_lib = "/usr/lib/x86_64-linux-gnu/libvisa.so.20.0.0"

test_instr_name = "visa://{addr}/GPIB0::INTFC".format(addr=ip_addr)

instr_2400 = "visa://{addr}/GPIB0::24::INSTR".format(addr=ip_addr)
