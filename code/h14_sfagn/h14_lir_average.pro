pro h14_lir_average,z_range,loglagn_out,loglir_ave_out,model=model,print=print

;INPUTS: z_range [zhi, zlo] (0 < z < 3)
;OUTPUTS: loglagn: log(L_AGN [erg/s]); loglir_ave: 'log(<L_IR [erg/s]>)'
;OPTIONAL: model: model accretion rate distribution (default is "fiducial")
;PRINT: prints to standard output

if n_elements(model) eq 0 then model='fiducial'

;restore the model sources
restore,'h14_sfagn_'+model+'.sav'


ind_z = where(zv ge z_range[0] and zv le z_range[1])

if n_elements(ind_z) eq 1 then ind_z =[ind_z,ind_z]
lir_ave_z = sum(lir_ave[*,ind_z],1)/double(n_elements(ind_z))

iagn = where(loglagnv gt 41.)

loglir_ave_out = alog10(lir_ave_z[iagn])
loglagn_out = loglagnv[iagn]

if keyword_set(print) then print,'Output for Hickox et al. (2014)'
print,'Model: '+model
print,'z range: '+strjoin(string(z_range))

if keyword_set(print) then begin 
print, 'log(L_AGN [erg/s])','log(<L_IR [erg/s]>)'



for i=0,n_elements(loglagn_out)-1 do begin

print,loglagn_out[i],loglir_ave_out[i]
endfor
endif


end
