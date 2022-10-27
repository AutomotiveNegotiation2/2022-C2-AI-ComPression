
import matplotlib.pyplot as plt
import matplotlib
from collections import deque
import numpy as np

plt.style.use('fivethirtyeight')
matplotlib.use('TkAgg')



def view(AI_res_data,AL_res_data,now_spd_list,delay_list):
    # compression result viewer
    # AI_res_data : Dzip's space savings
    # AL_res_data : zlib'x space savings
    # space savings = 1 - ( after data size / before data size) * 100
    # now_spd_list : car's speed
    # delay_list : hybrid model converting delay time ( AI <-> Rule )
    comp_num = 0
    speed_num = 0
    spd_num_q=deque([])
    spd_q = deque([])
    hybrid_q = deque([])
    comp_num_q = deque([])
    ai_saving_space_q = deque([])
    al_saving_space_q = deque([])

    fig, ax = plt.subplots(nrows=2,ncols=1,gridspec_kw={'height_ratios' : [3,1]}, figsize=(10,10))
    delay_num = -1
    delay_num_diff = -1
    while True:
        if now_spd_list:
            spd_num_q.append(speed_num)
            spd_q.append( np.mean(now_spd_list[0]) )

            if speed_num > 20:
                spd_num_q.popleft()
                spd_q.popleft()
            ax[1].cla()
            ax[1].plot(spd_num_q,spd_q,label = f"velocity : {str(np.mean(spd_q))[:4] } km/h",color = "red",linewidth = 2)
            ax[1].text(spd_num_q[-1],spd_q[-1],str(spd_q[-1])[:4] +"km/h",color = "red", fontsize = 10)
            if spd_q[-1] >0:
                ax[1].set_title("STATE GRAPH(DYNAMIC)")
            else:
                ax[1].set_title("STATE GRAPH(STATIC)")
            ax[1].legend(fontsize = 12)
            ax[1].set(ylabel="VELOCITY[km/h]",xlabel = "TIME(sec)")
            if spd_num_q:
                ax[1].set_xlim([spd_num_q[0],spd_num_q[-1]+1] )
                ax[1].set_ylim([-5,100])
                ax[1].set_xticks( range(spd_num_q[0],spd_num_q[-1]+1))
            plt.pause(0.0001)
            del now_spd_list[0]
            speed_num += 1

        if AI_res_data and AL_res_data :
            AI_savingspace = AI_res_data[0]
            AL_savingspace = AL_res_data[0]
            if AI_res_data[0] == "break":
                break
            try:
                print("COMP_ID : {0}, METHOD : {1}, SPACE_SAVINGS : {2:2.2f} %, COMPRESSING_TIME : {3:0.4f} sec".format(AI_savingspace[0],AI_savingspace[1],AI_savingspace[2],AI_savingspace[3]))
                print("COMP_ID : {0}, METHOD : {1}, SPACE_SAVINGS : {2:2.2f} %, COMPRESSING_TIME : {3:0.4f} sec".format(AL_savingspace[0],AL_savingspace[1],AL_savingspace[2],AL_savingspace[3]))
            except Exception as e:
                print(f"ERROR_{e}")
                break    
            comp_num_q.append(comp_num)
            ai_saving_space_q.append(AI_savingspace[2])
            al_saving_space_q.append(AL_savingspace[2])

            delay_time = delay_list[0]
            if AL_savingspace[-1] == "dynamic":
                hybrid_q.append(AI_savingspace[2]-0.05)
            else:
                hybrid_q.append(AL_savingspace[2]-0.07)
            if comp_num > 20:
                comp_num_q.popleft()
                ai_saving_space_q.popleft()
                al_saving_space_q.popleft()
                hybrid_q.popleft()

            ax[0].cla()
            ax[0].plot(comp_num_q,ai_saving_space_q,label = f"AI : {str(np.mean(ai_saving_space_q))[:4] } %",color = "red",linewidth = 2)
            ax[0].plot(comp_num_q,al_saving_space_q,label = f"RULE : {str(np.mean(al_saving_space_q))[:4] } %", color = "green",linewidth = 2)
            ax[0].plot(comp_num_q,hybrid_q,label = f"HYBRID : {str(np.mean(hybrid_q))[:4] } %", color = "blue",linewidth = 3)
            ax[0].text(comp_num_q[-1],ai_saving_space_q[-1],str(AI_savingspace[2])[:4] + "%",color = "red", fontsize = 10)
            ax[0].text(comp_num_q[-1],al_saving_space_q[-1],str(AL_savingspace[2])[:4] + "%",color = "green",fontsize = 10)

            if (delay_time > 0.0):
                delay_num = comp_num_q[-1]
                delay_num_diff = delay_num - delay_time*0.001
            if delay_num in comp_num_q:
                ax[0].axvspan(delay_num_diff, delay_num)
                ax[0].text(delay_num,75.0,"delay_time\n"+str( (delay_num - delay_num_diff)*1000 )[:3] + "[msec]",color = "blue",fontsize = 10)
            ax[0].set_title("COMPRESSION GRAPH")
            ax[0].legend(fontsize = 12)
            
            ax[0].set(ylabel = "SPACE_SAVINGS(%)",xlabel = "COMPRESS TIME(SEC)")
            if comp_num_q:
                ax[0].set_xlim([comp_num_q[0],comp_num_q[-1]+1])
                ax[0].set_ylim([70,85])
                ax[0].set_xticks( range(comp_num_q[0],comp_num_q[-1]+1))
            plt.tight_layout()
            plt.pause(0.0001)
            del delay_list[0]
            del AI_res_data[0]
            del AL_res_data[0]
            comp_num += 1
    print("viewer END")