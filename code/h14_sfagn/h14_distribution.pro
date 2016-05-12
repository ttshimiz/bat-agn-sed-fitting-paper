pro h14_distribution,z_range,loglum_range,loglum_out,dens_out,input_type=input_type,model=model,print=print

;INPUT TYPE
;input_type == 0 --> input is log(L_AGN [erg/s]), output is distribution in log(L_IR [L_sun])
;input_type == 1 --> input is log(L_IR [L_sun]), output is distribution in log(L_AGN [erg/s])

;INPUTS: z_range [zhi, zlo] (0 < z < 3)
; loglum_range [loglum_hi, loglum_lo] (9 < loglum < 14 for log_LIR; 40 < loglum < 47 for log_Lagn)

;
;OUTPUTS: loglum_out: log(luminosity) array for output; dens_out: number density in Mpc^-3 dex^-1
;
;OPTIONAL: model: model accretion rate distribution (default is "fiducial"); print: prints to standard output


if n_elements(input_type) eq 0 then input_type = 0

if n_elements(model) eq 0 then model='fiducial'


;restore the model sources
restore,'h14_sfagn_'+model+'.sav'

ind_z = where(zv ge z_range[0] and zv le z_range[1])

if n_elements(ind_z) eq 1 then ind_z =[ind_z,ind_z]

nagn_zv_z = sum(num_agnz[*,*,ind_z],2)/double(n_elements(ind_z))

case input_type of

0: begin

ind_lx = where(loglagnv ge loglum_range[0] and loglagnv le loglum_range[1])



nagn_zv_z_l = sum(nagn_zv_z[*,ind_lx,*],1)

dens_out = nagn_zv_z_l

loglum_out = loglirv
l_type = 'log(L_AGN [erg/s])'
l_type_in = 'log(L_IR [L_sun])'
n_type = 'log(phi [Mpc^-3 dex^-1])'
end

1: begin

ind_lir = where(loglirv ge loglum_range[0] and loglirv le loglum_range[1])

nagn_zv_z_l = sum(nagn_zv_z[ind_lir,*,*],0)

dens_out = nagn_zv_z_l

loglum_out = loglagnv

l_type = 'log(L_IR [L_sun])'
l_type_in = 'log(L_AGN [erg/s])'
n_type = 'log(phi [Mpc^-3 dex^-1])'
end

endcase



if keyword_set(print) then print,'Output for Hickox et al. (2014)'
print,'Model: '+model
print,'z range: '+strjoin(string(z_range))
print,'input luminosity range: '+l_type_in+strjoin(string(loglum_range))

if keyword_set(print) then begin
print,l_type, n_type

for i=0,n_elements(loglum_out)-1 do begin

print,loglum_out[i],dens_out[i]
endfor
endif

end
