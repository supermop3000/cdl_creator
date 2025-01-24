import os
import re

directory = 'edls'

template = '''<?xml version="1.0" encoding="UTF-8"?>
<ColorDecisionList xmlns="urn:ASC:CDL:v1.01">
	<ColorDecision>
		<ColorCorrection id="{}">
			<SOPNode>
				<Slope>{}</Slope>
				<Offset>{}</Offset>
				<Power>{}</Power>
			</SOPNode>
			<SatNode>
				<Saturation>{}</Saturation>
			</SatNode>
		</ColorCorrection>
	</ColorDecision>
</ColorDecisionList>'''

def get_sop(data):
    # Define a regular expression pattern to match values inside parentheses
    # Use regular expressions to extract values between parentheses
    pattern = r"\((.*?)\)"
    matches = re.findall(pattern, data)

    # Extract individual values from each match
    var1 = tuple(float(x) for x in matches[0].split())
    var2 = tuple(float(x) for x in matches[1].split())
    var3 = tuple(float(x) for x in matches[2].split())

    return var1, var2, var3

def write_cdl_info(clip_name, slope, offset, power, sat):
    print(clip_name)
    print("SLOPE")
    print(slope[0])

    xml_content = template.format(clip_name, ' '.join(str(val) for val in slope), ' '.join(str(val) for val in offset),
                                  ' '.join(str(val) for val in power), sat)

    print("- - - - END EXTRACRT - - - -")

    folder = 'cdls'
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Save the XML content to a file in the 'cdl' folder
    filename = os.path.join(folder, "{}.cdl".format(clip_name))
    with open(filename, 'w') as file:
        file.write(xml_content)

def create_cdl_from_edl():
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)

        if os.path.isfile(f):
            print(f)

        # f = 'C:\\Users\ccort\Desktop\cdl_creator\edls\IDL_105_060_010-070.edl'
        # f = 'C:\\Users\ccort\Desktop\cdl_creator\edls\IDL_105_004_010.edl'
        # f = 'C:\\Users\ccort\Desktop\cdl_creator\edls\IDL_105_032_010-020.edl'
        # f = 'C:\\Users\ccort\Desktop\cdl_creator\edls\IDL_105_007_100 REF.edl'

        with open(f) as open_edl:
            print("FILE IS: " + str(f))
            event_data = []
            current_event = {}

            for line in open_edl:
                if line.startswith("000"):
                    if current_event:
                        event_data.append(current_event)
                    current_event = {"Event": line.strip()}
                elif line.startswith("*FROM CLIP NAME:"):
                    current_event["Clip Name"] = line.split(":")[1].strip()
                elif line.startswith("*ASC_SOP"):
                    values = re.findall(r"\((.*?)\)", line)
                    current_event["ASC_SOP"] = [tuple(map(float, v.split())) for v in values]
                elif line.startswith("*ASC_SAT"):
                    current_event["ASC_SAT"] = float(line.split()[1])

            # Append the last event
            if current_event:
                event_data.append(current_event)

            # Print the grouped data
            for event in event_data:
                print(event)
                try:
                    print("TEST")
                    clip_name = event["Clip Name"]
                    slope = event["ASC_SOP"][0]
                    offset = event["ASC_SOP"][1]
                    power = event["ASC_SOP"][2]
                    sat = event["ASC_SAT"]

                    write_cdl_info(clip_name, slope, offset, power, sat)

                    print("Event:", event["Event"])
                    print("Clip Name:", event["Clip Name"])
                    print("ASC_SOP:", event["ASC_SOP"])
                    print("ASC_SAT:", event["ASC_SAT"])
                    print()

                except KeyError:
                    print("KEY ERROR")
                    pass

            # for line in open_edl:
            #     if line.startswith('*FROM CLIP NAME:'):
            #         clip_name_line = line
            #         clip_name = line.split(":  ", 1)[1]
            #         clip_name = clip_name.strip()
            #     if line.startswith('*ASC_SOP'):
            #         sop_line = line
            #         slope, offset, power = get_sop(sop_line)
            #     if line.startswith('*ASC_SAT'):
            #         sat_line = line
            #         sat = sat_line.split("T ", 1)[1]
            #         sat = sat.strip()
            #
            #     extract_cdl_info(clip_name, slope, offset, power, sat)

        # print(clip_name)
        # print("SLOPE")
        # print(slope[0])
        #
        # xml_content = template.format(clip_name, ' '.join(str(val) for val in slope), ' '.join(str(val) for val in offset),
        #                               ' '.join(str(val) for val in power), sat)
        #
        # print("- - - - END EXTRACRT - - - -")
        #
        # folder = 'cdls'
        # if not os.path.exists(folder):
        #     os.makedirs(folder)
        #
        # # Save the XML content to a file in the 'cdl' folder
        # filename = os.path.join(folder, "{}.cdl".format(clip_name))
        # with open(filename, 'w') as file:
        #     file.write(xml_content)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_cdl_from_edl()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
