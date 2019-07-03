# methane_injection_conc = [100,200,300] #Whatever vales you need
# hydrogen_injection_conc = [100.200,300] #whatever values you need
# test_counter = 1
#
# ##############################################33333
#  ###### Deprecated ##########
# #fill_methane_time = 0
# methane_correction_factor = 0.73#found it on MKS website
# methane_flow_rate = 10 #what the value on the MFC is set to
# #methane_injection_amount = methane_injection_conc / 500 # mL
# fill_methane_time = [0,0,0]
#
# for i in range(0, len(methane_injection_conc)):
#     fill_methane_time[i] = ((60 *(1/ methane_correction_factor ) *(methane_injection_conc[i]/500)/methane_flow_rate)


methane_injection_conc = [100,200,300]

methane_correction_factor = 0.73
methane_flow_rate = 10

fill_methane_time = [0,0,0]
divisor = 60/(500*methane_correction_factor*methane_flow_rate)

for i in range(0,len(methane_injection_conc)-1):
    fill_methane_time[i] = int(methane_injection_conc[i] * divisor)

print(fill_methane_time)
