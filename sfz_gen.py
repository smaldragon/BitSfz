import os
import random

REGION_NOTES = [
    (0,47), 
    (48,59),
    (60,71),
    (72,83),
    (84,96),
    (97,127)
]

def convert(value):
    value/=100
    value=value*value*value
    return value * 100
def generate_file(filename,directory,data):
    #os.makedirs(path, exist_ok=True)
    with open(f"{directory+'/'+filename}","w") as f:
        f.write("// Auto Generated file by sfz_gen.py\n")
        f.write(f"// {random.random()}\n")
        f.write("<control>\n")
        f.write("<global>\n")
        f.write("loop_mode=loop_continuous\n")
        for i,settings in enumerate(data):
            if settings["wave_editor"].wave_data != [0]*32:
                f.write("<group>\n")
                f.write(f'ampeg_delay={convert(settings["ampeg_delay"].value)}\n')
                f.write(f'ampeg_attack={convert(settings["ampeg_attack"].value)}\n')
                f.write(f'ampeg_hold={convert(settings["ampeg_hold"].value)}\n')
                f.write(f'ampeg_decay={convert(settings["ampeg_decay"].value)}\n')
                f.write(f'ampeg_sustain={settings["ampeg_sustain"].value}\n')
                f.write(f'ampeg_release={convert(settings["ampeg_release"].value)}\n')

                f.write(f'pitchlfo_delay={convert(settings["pitchlfo_delay"].value)}\n')
                f.write(f'pitchlfo_fade={convert(settings["pitchlfo_fade"].value)}\n')
                f.write(f'pitchlfo_depth={settings["pitchlfo_depth"].value}\n')
                f.write(f'pitchlfo_freq={settings["pitchlfo_freq"].value}\n')

                f.write(f'tune={(settings["tune"].value-50)*2}\n')
                f.write(f'pan={settings["pan"].value-50}\n')

                for u in range(6):
                    l = ["A","B","C","D"][i]
                    f.write(f"<region> sample=samples/live_{l}_{u}.wav lokey={REGION_NOTES[u][0]} hikey={REGION_NOTES[u][1]} pitch_keycenter={57}")
                    f.write("\n")