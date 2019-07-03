methane_injection_conc = [100,200,300] #Whatever vales you need
hydrogen_injection_conc = [100.200,300] #whatever values you need
test_counter = 1

##############################################33333
 ###### Deprecated ##########
#fill_methane_time = 0
methane_correction_factor = 0.73#found it on MKS website
methane_flow_rate = 10#what the value on the MFC is set to
#methane_injection_amount = methane_injection_conc / 500 # mL
mtime = [0,0,0]

for i in range(0,(len(methane_injection_conc))):
    mtime[i] = methane_injection_conc[i] * 5
# mtime[0] = methane_injection_conc[0] * 5
# mtime[1] = methane_injection_conc[1] * 5
# mtime[2] = methane_injection_conc[2] * 5
print(mtime)
