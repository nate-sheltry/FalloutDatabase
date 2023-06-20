import requests, time
from bs4 import BeautifulSoup

fallout_2_url = "https://fallout.fandom.com/wiki/Resources:Fallout_2_critter_statistics"
fallout_1_url = "https://fallout.fandom.com/wiki/Resources:Fallout_critter_statistics"

indexData = []
data = []
path = "D:/JavaScript Projects/FalloutAPI/"
    


def fetchData(url, append_name = ""):
    # Send a GET request to the URL
    response = requests.get(url)
    # Process data recieve as html
    soup = BeautifulSoup(response.content, "html.parser")
    #find the table, in this case the "critter statistics table"
    table = soup.find("table", {"class": "va-table"})
    
    # Extract the data from the table rows
  
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) > 0:
            shouldContinue = True
            cells = ([cell.text.strip() for cell in cells])
            name = f'{cells[1].replace("?", "X").replace("/", "").replace("|", "").replace(":", "").replace("*", "^")}'
            if("(don't use)" in name):
                continue
            special = [int(cells[2]), int(cells[3]), int(cells[4]), int(cells[5]), int(cells[6]), int(cells[7]), int(cells[8])]
            secStat = [int(cells[9]), int(cells[10]), int(cells[11]), int(cells[13]), int(cells[14]), int(cells[15])]
            gmInfo = [int(cells[16]), int(cells[23]), int(cells[24])]
            dmgThr = [cells[25].replace("|"," | "), cells[26].replace("|"," | "), cells[27].replace("|"," | "), cells[28].replace("|"," | "), cells[29].replace("|"," | "), cells[30].replace("|"," | "), cells[31].replace("|"," | ")]
            skills =[int(cells[17]), int(cells[18]), int(cells[19]),
                        int(cells[20]), int(cells[21]), int(cells[22])]
            
            critterStats = ('\t"special": {"S":' + f'{special[0]}, "P": ' + f'{special[1]}, "E": ' + f'{special[2]}, "C": ' + f'{special[3]}, "I": ' + f'{special[4]}, "A": '+ f'{special[5]}, "L": '+ f'{special[6]}' +'},\n'+
                    '\t"secondaryStats": {"AP":' + f'{secStat[0]}, '+'"AC":' + f'{secStat[1]}, '+'"HP":' + f'{secStat[2]}, '+'"MD":' + f'{secStat[3]}, '+'"CC":' + f'{secStat[4]}, '+'"SQ":'+ f'{secStat[5]}' + '},\n'+
                    '\t"gmInfo": {"XP": ' + f'{gmInfo[0]}, ' + '"rad_-Res_": ' + f'{gmInfo[1]},' + '"pois_-Res_": ' + f'{gmInfo[2]}' + '},\n'+
                    '\t"damageThreshold": {"norm": ' + f'"{dmgThr[0]}", ' + '"laser": ' + f'"{dmgThr[1]}", ' + '"fire": ' + f'"{dmgThr[2]}", ' + '"plasma": ' + f'"{dmgThr[3]}", ' + '"elec_": ' + f'"{dmgThr[4]}", ' + '"expl_": ' + f'"{dmgThr[5]}", ' + '"EMP": ' + f'"{dmgThr[6]}"' + '},\n'+
                    '\t"skillsInfo": {"sm_-Guns": ' + f'{skills[0]}, ' + '"big-Guns": ' + f'{skills[1]}, ' + '"en_-Weap_": ' + f'{skills[2]}, ' + '"unarmed": ' + f'{skills[3]}, ' + '"melee": ' + f'{skills[4]}, ' + '"throw_": ' + f'{skills[5]}' + '}\n'
                    )
            
            for string in data:
                if(critterStats in string and name.replace(" ", "-").replace(".", "_").lower()[:-1] in string):
                    shouldContinue = False
                    break
                if(f'{name.replace(" ", "-").replace(".", "_").lower()}' in string):
                    print('contains')
                    if(' Alt.1' in name):
                        name = f'{name[:-6]} Alt.2'
                    elif(' Alt.2' in name):
                        name = f'{name[:-6]} Alt.3'
                    elif(' Alt.3' in name):
                        name = f'{name[:-6]} Alt.4'
                    elif(' Alt.4' in name):
                        name = f'{name[:-6]} Alt.5'
                    else:
                        name += ' Alt.1'
            if(shouldContinue == False):
                continue
            critter = ('{\n' + critterStats +'}')
            name = f'{name}{append_name}'
            data.append(f'\t"{name.replace(" ", "-").replace(".", "_").lower()}": {critter}')
            indexData.append(f'\t"{name.replace(" ", "-").replace(".", "_").lower()}": ' + '{\n' + '\t\t"name": ' + f'"{name}",\n' + '\t\t"url": ' + f'"https://nate-sheltry.github.io/FalloutDatabase/critter-data/{name.replace(" ", "-").replace(".", "_").lower()}.json"\n' + '\t},\n')
            with open(f'{path}database/critter-data/{name.replace(" ", "-").replace(".", "_").lower()}.json', 'w') as file:
                # Write the data to the file
                file.write(critter)
                file.close()

fetchData(fallout_2_url, " - Fallout 2")
fetchData(fallout_1_url, " - Fallout 1")


indexData.sort()# Print the extracted data
    


with open(f"{path}database/index-data.json", "w") as file:
    # Write the data to the file
    file.write("{\n")
    for row in indexData:
        file.write(row)
    file.seek(file.tell() - 3)
    file.write("\n}")
