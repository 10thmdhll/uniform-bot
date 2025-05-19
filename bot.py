import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
import os
import aiohttp
import asyncio
from dotenv import load_dotenv

# Functions
def trim(im):
    """Trim transparent edges of a ribbon."""
    bbox = im.getbbox()
    if bbox:
        return im.crop(bbox)
    return im
    
# Load environment variables
load_dotenv()

# === Template definitions ===
rank_templates = {
    'Col.': 'ranks/COL.png',
    'Lt. Col.': 'ranks/LTC.png',
    'CSM.': 'ranks/CSM.png',
    'Maj.': 'ranks/MAJ.png',
    'Cpt.': 'ranks/CPT.png',
    'SGM.': 'ranks/SGM.png',
    '1st Sgt.': 'ranks/1STSGT.png',
    'M/Sgt.': 'ranks/MSGT.png',
    '1Lt.': 'ranks/1LT.png',
    'CWO.': 'ranks/CWO.png',
    '2Lt.': 'ranks/2LT.png',
    'T/Sgt.': 'ranks/TSGT.png',
    'WO.': 'ranks/WO.png',
    'S/Sgt.': 'ranks/SSGT.png',
    'Sgt.': 'ranks/SGT.png',
    'Cpl.': 'ranks/CPL.png',
    'T/3': 'ranks/T3.png',
    'T/4': 'ranks/T4.png',
    'T/5': 'ranks/T5.png',
    'Pfc.': 'ranks/PFC.png',
    'Pvt.': 'ranks/PVT.png'
}
assignment_templates = {
    "Division Command": {"Assignment": "Division Command"},
    "Battalion Leadership": {"Assignment": "Battalion Command"},
    "Dog Company Leadership": {"Assignment": "Dog Company Command"},
    "Fox Company Leadership": {"Assignment": "Fox Company Command"},
    "DP1 - Leadership": {"Assignment": "Dog Company First Platoon Command"},
    "FP1 - Leadership": {"Assignment": "Fox Company First Platoon Command"},
    "FP2 - Leadership": {"Assignment": "Fox Company Second Platoon Command"},
    "DP1 - Infantry": {"Assignment": "Dog Company First Platoon Infantry"},
    "DP1 - Recon": {"Assignment": "Dog Company First Platoon Recon"},
    "DP1 - Logistics": {"Assignment": "Dog Company First Platoon Logistics"},
    "FP1 - Infantry": {"Assignment": "Fox Company First Platoon Infantry"},
    "FP2 - Infantry": {"Assignment": "Fox Company Second Platoon Infantry"},
    "FP2 - Recon": {"Assignment": "Fox Company Second Platoon Recon"},
    "FP2 - Armor": {"Assignment": "Fox Company Second Platoon Armor"}
    }
unitcoms_templates = {
    "Founders Silver Ribbon": 'awards/Founders1.png',
    "Founders Ribbon": 'awards/Founders.png',
    "ReClimb Unit Commendation": 'awards/ReClimb.png',
}

eib_templates = {
    'Combat Infantryman Badge': 'awards/CIB.png',
    'Expert Infantryman Badge': 'awards/EIB.png'
}

patch_templates = {
    "Ranger": 'awards/Ranger.png',
    "Recon": 'awards/Recon.png',
    "Pathfinder": 'awards/PF.png'
}

driver_templates = {
    "Driver - Tank Weapons": 'awards/TankWeapons.png',
    "Driver - Tracked": 'awards/DriverT.png',
    "Driver - Wheeled": 'awards/DriverW.png',
    "Driver - Mechanic": 'awards/Mechanic.png'
}

equal_templates = {
    "Expert - Artillery": 'awards/FieldArtillery.png',
    "Expert - Anti Tank": 'awards/AT.png',
    "Expert - Auto Rifle": 'awards/AutoRifle.png',
    "Expert - Grenade": 'awards/Grenade.png',
    "Expert - MG": 'awards/MG.png',
    "Expert - Pistol": 'awards/Pistol.png',
    "Expert - Rifle": 'awards/Rifle.png',
    "Expert - Scoped Rifle": 'awards/ScopedRifle.png',
    "Expert - SMG": 'awards/SMG.png'
}

squal_templates = {
    "Sharpshooter - Artillery": 'awards/FieldArtillery.png',
    "Sharpshooter - Anti Tank": 'awards/AT.png',
    "Sharpshooter - Auto Rifle": 'awards/AutoRifle.png',
    "Sharpshooter - Grenade": 'awards/Grenade.png',
    "Sharpshooter - MG": 'awards/MG.png',
    "Sharpshooter - Pistol": 'awards/Pistol.png',
    "Sharpshooter - Rifle": 'awards/Rifle.png',
    "Sharpshooter - Scoped Rifle": 'awards/ScopedRifle.png',
    "Sharpshooter - SMG": 'awards/SMG.png'
}

mqual_templates = {
    "Marksman - Artillery": 'awards/FieldArtillery.png',
    "Marksman - Anti Tank": 'awards/AT.png',
    "Marksman - Auto Rifle": 'awards/AutoRifle.png',
    "Marksman - Grenade": 'awards/Grenade.png',
    "Marksman - MG": 'awards/MG.png',
    "Marksman - Pistol": 'awards/Pistol.png',
    "Marksman - Rifle": 'awards/Rifle.png',
    "Marksman - Scoped Rifle": 'awards/ScopedRifle.png',
    "Marksman - SMG": 'awards/SMG.png'
}

award_templates = {
    'Distinguished Service Cross': 'awards/DSC1.png',
    'Distinguished Service Medal': 'awards/DSM1.png',
    'Silver Star': 'awards/SS1.png', 
    'Bronze Star - 10': 'awards/BS10.png',
    'Bronze Star - 9': 'awards/BS9.png',
    'Bronze Star - 8': 'awards/BS8.png',
    'Bronze Star - 7': 'awards/BS7.png',
    'Bronze Star - 6': 'awards/BS6.png',
    'Bronze Star - 5': 'awards/BS5.png',
    'Bronze Star - 4': 'awards/BS4.png',
    'Bronze Star - 3': 'awards/BS3.png',
    'Bronze Star - 2': 'awards/BS2.png',
    'Bronze Star - 1': 'awards/BS1.png',
    'Purple Heart - 10': 'awards/PH9.png',
    'Purple Heart - 9': 'awards/PH9.png',
    'Purple Heart - 8': 'awards/PH8.png',
    'Purple Heart - 7': 'awards/PH7.png',
    'Purple Heart - 6': 'awards/PH6.png',
    'Purple Heart - 5': 'awards/PH5.png',
    'Purple Heart - 4': 'awards/PH4.png',
    'Purple Heart - 3': 'awards/PH3.png',
    'Purple Heart - 2': 'awards/PH2.png',
    'Purple Heart - 1': 'awards/PH1.png',
    'Meritorious Service Medal - 5': 'awards/MSM5.png',
    'Meritorious Service Medal - 4': 'awards/MSM4.png',
    'Meritorious Service Medal - 3': 'awards/MSM3.png',
    'Meritorious Service Medal - 2': 'awards/MSM2.png',
    'Meritorious Service Medal - 1': 'awards/MSM1.png',
    'Army Commendation Medal - 10': 'awards/ACOM10.png',
    'Army Commendation Medal - 9': 'awards/ACOM9.png',
    'Army Commendation Medal - 8': 'awards/ACOM8.png',
    'Army Commendation Medal - 7': 'awards/ACOM7.png',
    'Army Commendation Medal - 6': 'awards/ACOM6.png',
    'Army Commendation Medal - 5': 'awards/ACOM5.png',
    'Army Commendation Medal - 4': 'awards/ACOM4.png',
    'Army Commendation Medal - 3': 'awards/ACOM3.png',
    'Army Commendation Medal - 2': 'awards/ACOM2.png',
    'Army Commendation Medal - 1': 'awards/ACOM1.png',
    'Army Achievement Medal - 10': 'awards/AAM10.png',
    'Army Achievement Medal - 9': 'awards/AAM9.png',
    'Army Achievement Medal - 8': 'awards/AAM8.png',
    'Army Achievement Medal - 7': 'awards/AAM7.png',
    'Army Achievement Medal - 6': 'awards/AAM6.png',
    'Army Achievement Medal - 5': 'awards/AAM5.png',
    'Army Achievement Medal - 4': 'awards/AAM4.png',
    'Army Achievement Medal - 3': 'awards/AAM3.png',
    'Army Achievement Medal - 2': 'awards/AAM2.png',
    'Army Achievement Medal - 1': 'awards/AAM1.png',
    'Army Good Conduct Medal - 10': 'awards/AGC10.png',
    'Army Good Conduct Medal - 9': 'awards/AGC9.png',
    'Army Good Conduct Medal - 8': 'awards/AGC8.png',
    'Army Good Conduct Medal - 7': 'awards/AGC7.png',
    'Army Good Conduct Medal - 6': 'awards/AGC6.png',
    'Army Good Conduct Medal - 5': 'awards/AGC5.png',
    'Army Good Conduct Medal - 4': 'awards/AGC4.png',
    'Army Good Conduct Medal - 3': 'awards/AGC3.png',
    'Army Good Conduct Medal - 2': 'awards/AGC2.png',
    'Army Good Conduct Medal - 1': 'awards/AGC1.png',
    'American Defense Service Medal': 'awards/AD.png',
    'American Campaign Medal - 5': 'awards/AC5.png',
    'American Campaign Medal - 4': 'awards/AC4.png',
    'American Campaign Medal - 3': 'awards/AC3.png',
    'American Campaign Medal - 2': 'awards/AC2.png',
    'American Campaign Medal - 1': 'awards/AC1.png',
    'World War II Victory Medal': 'awards/WWIIV.png',
    'Army of Occupation Medal': 'awards/Occupation.png',
    "Gold Lifesaving Medal": 'awards/GLS.png',
    "Silver Lifesaving Medal": 'awards/SLS.png',
    'Medal of Humane Action': 'awards/HA.png',
    'Armed Forces Service Medal': 'awards/AFSM.png',
    'NCO Development Ribbon - Infantry': 'awards/NCO.png',
    'NCO Development Ribbon - Armor': 'awards/NCOArmor.png',
    'Army Service Ribbon': 'awards/ASR.png'
}

# === Generate uniform card image ===
def generate_uniform_card(user_name, rank_roles, assign_role, assign_data, award_roles, eib_roles, uc_roles, patch_roles, driver_roles, equal_roles, squal_roles, mqual_roles, filename):
    width, height = 1800, 1200
    
    # Background Color
    #img = Image.new("RGB", (width, height), color=(34, 45, 30))
    img = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw background silhouette first so icons appear on top
    assign_value = assign_data.get("Assignment", "")
    armor_assigned = ["Fox Company Second Platoon Armor"]
    
    if assign_value in armor_assigned:
        sil_path = "Armor.png"
    else:
        sil_path = "Infantry.png"
        
    if os.path.exists(sil_path):
        try:
            sil = Image.open(sil_path).resize((1024, 1536))
            img.paste(sil, (800, 100), sil.convert("RGBA"))
        except Exception:
            pass

    # Load fonts
    font_path = "DejaVuSansMono.ttf"
    try:
        header_font = ImageFont.truetype(font_path, 32)
        text_font = ImageFont.truetype(font_path, 24)
        small_font = ImageFont.truetype(font_path, 18)
    except IOError:
        header_font = text_font = small_font = ImageFont.load_default()

    # Header
    draw.text((20, 20), f"Uniform Issued to: {user_name}", fill="white", font=header_font)
    y = 80

    # Rank section
    if rank_roles:
        for rank_name in rank_roles:
            draw.text((40, y), f"Rank: {rank_name}", fill="white", font=header_font)
            y += 30     
            y += 40

    # Assignment section
    if assign_role and assign_data:
        y += 40
        assign_value = assign_data.get("Assignment", "")
        draw.text((40, y), f"Assignment: {assign_value}", fill="white", font=header_font)
        y += 40

    # Awards section
    y += 60
    draw.text((40, y), "Awards:", fill="white", font=header_font)
    y += 40
    
    # List award names text
    list_y = y
    
    # List EIB
    if eib_roles:
        for eib in eib_roles:
            draw.text((40, list_y), f"- {eib}", fill="white", font=small_font)
            list_y += 30     
            y += 40
    
    # List Ribbons    
    if award_roles:
        for aw in award_roles:
            draw.text((40, list_y), f"- {aw}", fill="white", font=small_font)
            list_y += 30     
            y += 40
    
    # List Patches
    if patch_roles:
        for p1 in patch_roles:
            draw.text((40, list_y), f"- {p1}", fill="white", font=small_font)
            list_y += 30     
            y += 40
        
    # List Unit Coms
    if uc_roles:
        for uc1 in uc_roles:
            draw.text((40, list_y), f"- {uc1}", fill="white", font=small_font)
            list_y += 30     
            y += 40
        
    # List Driver Quals
    if driver_roles:
        for dr1 in driver_roles:
            draw.text((40, list_y), f"- {dr1}", fill="white", font=small_font)
            list_y += 30     
            y += 40
    
    # List Expert Quals
    if equal_roles:
        for eq1 in equal_roles:
            draw.text((40, list_y), f"- {eq1}", fill="white", font=small_font)
            list_y += 30     
            y += 40
        
    # List Sharpshooter Quals
    if squal_roles:
        for ss1 in squal_roles:
            draw.text((40, list_y), f"- {ss1}", fill="white", font=small_font)
            list_y += 30     
            y += 40
        
    # List Marksman Quals
    if mqual_roles:
        for mq1 in mqual_roles:
            draw.text((40, list_y), f"- {mq1}", fill="white", font=small_font)
            list_y += 30     
            y += 40
    
    # Save final image
    img.save(filename)

# === Bot setup ===
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

GUILD_ID = 1366830976369557654

@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    tree.copy_global_to(guild=guild)
    synced = await tree.sync(guild=guild)
    print(f"Synced {len(synced)} commands to guild {GUILD_ID}")
    print(f"Logged in as {bot.user.name}")

@tree.command(name="uniform")
async def uniform(ctx):
    member = ctx.user
    filename = f"{member.name}_uniform.png"
    filename_r = f"{member.name}_r.png"
    
    # Gather all roles except @everyone
    all_roles = sorted([r for r in member.roles if r.name != "@everyone"], key=lambda r: r.position)

    # Determine primary rank and assignment
    rank_roles = [r for r in reversed(all_roles) if r.name in rank_templates]
    assign_roles = [r for r in reversed(all_roles) if r.name in assignment_templates]
    assign_role = assign_roles[0].name if assign_roles else None
    assign_data = assignment_templates.get(assign_role, {}) if assign_role else {}
    
    eib_roles = [r.name for r in reversed(all_roles) if r.name in eib_templates]
    award_roles = [r.name for r in reversed(all_roles) if r.name in award_templates]
    uc_roles = [r.name for r in reversed(all_roles) if r.name in unitcoms_templates]
    patch_roles = [r.name for r in reversed(all_roles) if r.name in patch_templates]
    driver_roles = [r.name for r in reversed(all_roles) if r.name in driver_templates]
    equal_roles = [r.name for r in reversed(all_roles) if r.name in equal_templates]
    squal_roles = [r.name for r in reversed(all_roles) if r.name in squal_templates]
    mqual_roles = [r.name for r in reversed(all_roles) if r.name in mqual_templates]
              
    # Generate main image    
    generate_uniform_card(
        member.display_name,
        rank_roles,
        assign_role,
        assign_data,
        award_roles,
        eib_roles,
        uc_roles,
        patch_roles,
        driver_roles,
        equal_roles,
        squal_roles,
        mqual_roles,
        filename
    )
    
    # Grab the current background image
    bg = Image.open(filename).convert('RGBA')
    
    ##################################################################################
    # Rank roles
    shoulder_list = ['Col.','Lt. Col.', 'Maj.', 'Cpt.', '1Lt.', 'CWO.', '2Lt.', 'WO.']
    # Loop through roles
    if rank_roles:
        for index, role_name in enumerate(rank_roles):
            try:
                # Open ribbon/patch for the role
                role_image = Image.open(rank_templates[role_name.name]).convert('RGBA')
    
                # Optionally resize
                if role_name.name in shoulder_list:
                    x = 1080
                    y = 420
                    if role_name.name in ['1Lt.','2Lt.']:
                        role_image = role_image.resize((40,60), Image.Resampling.LANCZOS)
                    else:
                        role_image = role_image.resize((75, 75), Image.Resampling.LANCZOS)
                else:
                    role_image = role_image.resize((100, 120), Image.Resampling.LANCZOS)
                    x = 850
                    y = 480

                # Paste the role image onto background
                bg.paste(role_image, (x, y), mask=role_image)

            except FileNotFoundError:
                print(f"Image for role '{role_name}' not found. Skipping.")  
    ##################################################################################
    # EIB/CIB roles
    
    if eib_roles:
        # Loop through roles
        for index, role_name in enumerate(eib_roles):
            try:
                # Open ribbon/patch for the role
                role_image = Image.open(eib_templates[role_name]).convert('RGBA')
    
                # Optionally resize
                if role_name == 'Expert Infantryman Badge':
                    role_image = role_image.resize((150, 20), Image.Resampling.LANCZOS)
                if role_name == 'Combat Infantryman Badge':
                    role_image = role_image.resize((150, 35), Image.Resampling.LANCZOS)
                    
                # Calculate position 
                x = 1425 
                y = 380  
    
                # Paste the role image onto background
                bg.paste(role_image, (x, y), mask=role_image)
    
            except FileNotFoundError:
                print(f"Image for role '{role_name}' not found. Skipping.")  
                
    ##################################################################################
    # Patches
    if patch_roles:
       # Loop through roles
        for index, role_name in enumerate(patch_roles):
            try:
                # Open ribbon/patch for the role
                role_image = Image.open(patch_templates[role_name]).convert('RGBA')
    
                # Optionally resize
                if role_name == 'Pathfinder':
                    role_image = role_image.resize((40, 40), Image.Resampling.LANCZOS)
                    x = 1535
                    y = 405
                    bg.paste(role_image, (x, y), mask=role_image)
                if role_name == 'Ranger':
                    role_image = role_image.resize((110, 50), Image.Resampling.LANCZOS)
                    x = 1625 
                    y = 370
                    bg.paste(role_image, (x, y), mask=role_image)
                if role_name == 'Recon':
                    role_image = role_image.resize((110, 50), Image.Resampling.LANCZOS)
                    x = 1625
                    y = 400
                    bg.paste(role_image, (x, y), mask=role_image)
    
            except FileNotFoundError:
                print(f"Image for role '{role_name}' not found. Skipping.")  
        
    ###################################################################################
    # Ribbon roles
    ribbon_width = 100
    ribbon_height = 35
    ribbons_per_row = 3
    
    if award_roles:
        ribbons = []
        for role in award_roles:
            role_name = role
            if role_name in award_templates:
                img_path = award_templates[role_name]
                img = Image.open(img_path)
                ribbons.append(img)
    
        if not ribbons:
            print("You don't have any ribbons assigned to you")
            
        # Trim all ribbons first
        ribbons = [trim(ribbon) for ribbon in ribbons]
    
        # Count and calculate
        num_ribbons = len(ribbons)
        rows = (num_ribbons + ribbons_per_row - 1) // ribbons_per_row  # ceiling division
        rack_width = min(ribbons_per_row, num_ribbons) * ribbon_width
        rack_height = rows * ribbon_height
    
        # Create blank rack
        rack = Image.new('RGBA', (rack_width, rack_height), (255, 255, 255, 0))
    
        # Reverse ribbons for right-to-left, bottom-to-top stacking
        ribbons = list(reversed(ribbons))

        # Build the rack
        for index, ribbon in enumerate(ribbons):
            row = (rows - 1) - (index // ribbons_per_row)  # bottom up
            col = ribbons_per_row - 1 - (index % ribbons_per_row)  # right to left

            # Default x, y position
            x = col * ribbon_width
            y = row * ribbon_height

            # Center the top row if incomplete
            if row == 0:
                ribbons_in_top_row = num_ribbons % ribbons_per_row
                if ribbons_in_top_row == 0:
                    ribbons_in_top_row = ribbons_per_row

                total_row_width = ribbons_in_top_row * ribbon_width
                offset = (rack_width - total_row_width) // 2

                x = (col - (ribbons_per_row - ribbons_in_top_row)) * ribbon_width + offset
            else:
                x = col * ribbon_width
            
            # Resize ribbon to fit exactly if needed
            ribbon = ribbon.resize((ribbon_width, ribbon_height))

            # Paste ribbon
            rack.paste(ribbon, (x, y), mask=ribbon if ribbon.mode == 'RGBA' else None)

        # Draw a black frame around the rack
        draw = ImageDraw.Draw(rack)
        draw.rectangle([(0, 0), (rack_width -1, rack_height -1)], outline="black", width=0)
    
        rackname = f"{member.name}_ribbons.png"
        rack.save(rackname)

        # Set Rack Location
        rack_x = 1380
        rack_y = 540 - rack_height + (rows * 20)

        # Ribbon Scale by a factor 
        rscale_factor = 0.6

        # Calculate Ribbon new size
        new_width = int(rack.width * rscale_factor)
        new_height = int(rack.height * rscale_factor)

        # Resize the rack
        rack = rack.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
        # Place the rack on the image
        bg.paste(rack, (rack_x, rack_y), mask=rack)
    
    ###################################################################################
    # Unit Coms
    ribbon_width = 100
    ribbon_height = 35
    ribbons_per_row = 3
    
    if uc_roles:
        ribbons = []
        for role in uc_roles:
            role_name = role
            if role_name in unitcoms_templates:
                img_path = unitcoms_templates[role_name]
                img = Image.open(img_path)
                ribbons.append(img)
    
        if not ribbons:
            print("You don't have any unit coms assigned to you")
    
        # Trim all ribbons first
        ribbons = [trim(ribbon) for ribbon in ribbons]

        # Count and calculate
        num_ribbons = len(ribbons)
        rows = (num_ribbons + ribbons_per_row - 1) // ribbons_per_row  # ceiling division
        rack_width = min(ribbons_per_row, num_ribbons) * ribbon_width
        rack_height = rows * ribbon_height

        # Create blank rack
        rack = Image.new('RGBA', (rack_width, rack_height), (255, 255, 255, 0))

        # Reverse ribbons for right-to-left, bottom-to-top stacking
        ribbons = list(reversed(ribbons))

        # Build the rack
        for index, ribbon in enumerate(ribbons):
            row = (rows - 1) - (index // ribbons_per_row)  # bottom up
            col = ribbons_per_row - 1 - (index % ribbons_per_row)  # right to left

            # Default x, y position
            x = col * ribbon_width
            y = row * ribbon_height

            # Center the top row if incomplete
            if row == 0:
                ribbons_in_top_row = num_ribbons % ribbons_per_row
                if ribbons_in_top_row == 0:
                    ribbons_in_top_row = ribbons_per_row

                total_row_width = ribbons_in_top_row * ribbon_width
                offset = (rack_width - total_row_width) // 2

                x = (col - (ribbons_per_row - ribbons_in_top_row)) * ribbon_width + offset
            else:
                x = col * ribbon_width
            
            # Resize ribbon to fit exactly if needed
            ribbon = ribbon.resize((ribbon_width, ribbon_height))

            # Paste ribbon
            rack.paste(ribbon, (x, y), mask=ribbon if ribbon.mode == 'RGBA' else None)

        # Draw a black frame around the rack
        draw = ImageDraw.Draw(rack)
        draw.rectangle([(0, 0), (rack_width -1, rack_height -1)], outline="black", width=0)
    
        rackname = f"{member.name}_ribbons.png"
        rack.save(rackname)

        # Set Rack Location
        rack_x = 1010
        rack_y = 530 - rack_height + (rows * 20)

        # Ribbon Scale by a factor 
        rscale_factor = 0.6

        # Calculate Ribbon new size
        new_width = int(rack.width * rscale_factor)
        new_height = int(rack.height * rscale_factor)

        # Resize the rack
        rack = rack.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
        # Place the rack on the image
        bg.paste(rack, (rack_x, rack_y), mask=rack)
    
    ##################################################################################
    # Dynamic starting points for qual area
    
    driverstart_x = 1325
    estart_x = 1325 #1425 
    sstart_x = 1325 #1525
    mstart_x = 1325 #1625 
           
    if driver_roles:
        estart_x = estart_x + 100
        sstart_x = sstart_x + 100
        mstart_x = mstart_x + 100
    if equal_roles:
        sstart_x = sstart_x + 100
        mstart_x = mstart_x + 100
    if squal_roles: 
        mstart_x = mstart_x + 100
    
    
    driverstart_y = 570
    estart_y = 570
    sstart_y = 570
    mstart_y = 570
        
    ##################################################################################
    # Driver roles
    if driver_roles:
        driverimg = Image.open("awards/Driver.png")
        driverimg = driverimg.resize((100, 100), Image.Resampling.LANCZOS)
        bg.paste(driverimg, (driverstart_x,driverstart_y), mask=driverimg)
    # Loop through roles
    
    if driver_roles:
        ribbon_width = 110
        ribbon_height = 35
        ribbons_per_row = 1
    
        ribbons = []
        for role in driver_roles:
            role_name = role
            if role_name in driver_templates:
                img_path = driver_templates[role_name]
                img = Image.open(img_path)
                ribbons.append(img)
    
        if not ribbons:
            print("You don't have any driver awards assigned to you")
        
        # Trim all ribbons first
        ribbons = [trim(ribbon) for ribbon in ribbons]
    
        # Count and calculate
        num_ribbons = len(ribbons)
        rows = (num_ribbons + ribbons_per_row - 1) // ribbons_per_row  # ceiling division
        rack_width = min(ribbons_per_row, num_ribbons) * ribbon_width
        rack_height = rows * ribbon_height
    
        # Create blank rack
        rack = Image.new('RGBA', (rack_width, rack_height), (255, 255, 255, 0))
    
        # Reverse ribbons for right-to-left, bottom-to-top stacking
        ribbons = list(reversed(ribbons))
    
        # Build the rack
        for index, ribbon in enumerate(ribbons):
            row = (rows - 1) - (index // ribbons_per_row)  # bottom up
            col = ribbons_per_row - 1 - (index % ribbons_per_row)  # right to left
    
            # Default x, y position
            x = col * ribbon_width
            y = row * ribbon_height - (row * 10)
    
            # Center the top row if incomplete
            if row == 0:
                ribbons_in_top_row = num_ribbons % ribbons_per_row
                if ribbons_in_top_row == 0:
                    ribbons_in_top_row = ribbons_per_row
    
                total_row_width = ribbons_in_top_row * ribbon_width
                offset = (rack_width - total_row_width) // 2
    
                x = (col - (ribbons_per_row - ribbons_in_top_row)) * ribbon_width + offset
            else:
                x = col * ribbon_width
                
            # Resize ribbon to fit exactly if needed
            ribbon = ribbon.resize((ribbon_width, ribbon_height))
    
            # Paste ribbon
            rack.paste(ribbon, (x, y), mask=ribbon if ribbon.mode == 'RGBA' else None)

        # Draw a black frame around the rack
        draw = ImageDraw.Draw(rack)
        draw.rectangle([(0, 0), (rack_width -1, rack_height -1)], outline="black", width=0)
    
        rackname = f"{member.name}_ribbons.png"
        rack.save(rackname)

        # Set Rack Location
        rack_x = driverstart_x + 15 
        rack_y = driverstart_y + 90

        # Ribbon Scale by a factor 
        rscale_factor = 0.7

        # Calculate Ribbon new size
        new_width = int(rack.width * rscale_factor)
        new_height = int(rack.height * rscale_factor)

        # Resize the rack
        rack = rack.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
        # Place the rack on the image
        bg.paste(rack, (rack_x, rack_y), mask=rack)
        
    ##################################################################################
    # Expert roles
    if equal_roles:
        driverimg = Image.open("awards/Expert.png")
        driverimg = driverimg.resize((100, 100), Image.Resampling.LANCZOS)
        bg.paste(driverimg, (estart_x,estart_y), mask=driverimg)
    # Loop through roles
    
    if equal_roles:
        ribbon_width = 110
        ribbon_height = 35
        ribbons_per_row = 1
    
        ribbons = []
        for role in equal_roles:
            role_name = role
            if role_name in equal_templates:
                img_path = equal_templates[role_name]
                img = Image.open(img_path)
                ribbons.append(img)
    
        if not ribbons:
            print("You don't have any expert awards assigned to you")
        
        # Trim all ribbons first
        ribbons = [trim(ribbon) for ribbon in ribbons]
    
        # Count and calculate
        num_ribbons = len(ribbons)
        rows = (num_ribbons + ribbons_per_row - 1) // ribbons_per_row  # ceiling division
        rack_width = min(ribbons_per_row, num_ribbons) * ribbon_width
        rack_height = rows * ribbon_height
    
        # Create blank rack
        rack = Image.new('RGBA', (rack_width, rack_height), (255, 255, 255, 0))
    
        # Reverse ribbons for right-to-left, bottom-to-top stacking
        ribbons = list(reversed(ribbons))
    
        # Build the rack
        for index, ribbon in enumerate(ribbons):
            row = (rows - 1) - (index // ribbons_per_row)  # bottom up
            col = ribbons_per_row - 1 - (index % ribbons_per_row)  # right to left
    
            # Default x, y position
            x = col * ribbon_width
            y = row * ribbon_height - (row * 10)
    
            # Center the top row if incomplete
            if row == 0:
                ribbons_in_top_row = num_ribbons % ribbons_per_row
                if ribbons_in_top_row == 0:
                    ribbons_in_top_row = ribbons_per_row
    
                total_row_width = ribbons_in_top_row * ribbon_width
                offset = (rack_width - total_row_width) // 2
    
                x = (col - (ribbons_per_row - ribbons_in_top_row)) * ribbon_width + offset
            else:
                x = col * ribbon_width
                
            # Resize ribbon to fit exactly if needed
            ribbon = ribbon.resize((ribbon_width, ribbon_height))
    
            # Paste ribbon
            rack.paste(ribbon, (x, y), mask=ribbon if ribbon.mode == 'RGBA' else None)

        # Draw a black frame around the rack
        draw = ImageDraw.Draw(rack)
        draw.rectangle([(0, 0), (rack_width -1, rack_height -1)], outline="black", width=0)
    
        rackname = f"{member.name}_ribbons.png"
        rack.save(rackname)

        # Set Rack Location
        rack_x = estart_x + 15 
        rack_y = estart_y + 90

        # Ribbon Scale by a factor 
        rscale_factor = 0.7

        # Calculate Ribbon new size
        new_width = int(rack.width * rscale_factor)
        new_height = int(rack.height * rscale_factor)

        # Resize the rack
        rack = rack.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
        # Place the rack on the image
        bg.paste(rack, (rack_x, rack_y), mask=rack)
    
    ##################################################################################
    # Sharpshooter roles
    if squal_roles:
        driverimg = Image.open("awards/Sharpshooter.png")
        driverimg = driverimg.resize((100, 100), Image.Resampling.LANCZOS)
        bg.paste(driverimg, (sstart_x,sstart_y), mask=driverimg)
    # Loop through roles
    
    if squal_roles:
        ribbon_width = 110
        ribbon_height = 35
        ribbons_per_row = 1
    
        ribbons = []
        for role in squal_roles:
            role_name = role
            if role_name in squal_templates:
                img_path = squal_templates[role_name]
                img = Image.open(img_path)
                ribbons.append(img)
    
        if not ribbons:
            print("You don't have any sharpshooter awards assigned to you")
        
        # Trim all ribbons first
        ribbons = [trim(ribbon) for ribbon in ribbons]
    
        # Count and calculate
        num_ribbons = len(ribbons)
        rows = (num_ribbons + ribbons_per_row - 1) // ribbons_per_row  # ceiling division
        rack_width = min(ribbons_per_row, num_ribbons) * ribbon_width
        rack_height = rows * ribbon_height
    
        # Create blank rack
        rack = Image.new('RGBA', (rack_width, rack_height), (255, 255, 255, 0))
    
        # Reverse ribbons for right-to-left, bottom-to-top stacking
        ribbons = list(reversed(ribbons))
    
        # Build the rack
        for index, ribbon in enumerate(ribbons):
            row = (rows - 1) - (index // ribbons_per_row)  # bottom up
            col = ribbons_per_row - 1 - (index % ribbons_per_row)  # right to left
    
            # Default x, y position
            x = col * ribbon_width
            y = row * ribbon_height - (row * 10)
    
            # Center the top row if incomplete
            if row == 0:
                ribbons_in_top_row = num_ribbons % ribbons_per_row
                if ribbons_in_top_row == 0:
                    ribbons_in_top_row = ribbons_per_row
    
                total_row_width = ribbons_in_top_row * ribbon_width
                offset = (rack_width - total_row_width) // 2
    
                x = (col - (ribbons_per_row - ribbons_in_top_row)) * ribbon_width + offset
            else:
                x = col * ribbon_width
                
            # Resize ribbon to fit exactly if needed
            ribbon = ribbon.resize((ribbon_width, ribbon_height))
    
            # Paste ribbon
            rack.paste(ribbon, (x, y), mask=ribbon if ribbon.mode == 'RGBA' else None)

        # Draw a black frame around the rack
        draw = ImageDraw.Draw(rack)
        draw.rectangle([(0, 0), (rack_width -1, rack_height -1)], outline="black", width=0)
    
        rackname = f"{member.name}_ribbons.png"
        rack.save(rackname)

        # Set Rack Location
        rack_x = sstart_x + 15 
        rack_y = sstart_y + 90

        # Ribbon Scale by a factor 
        rscale_factor = 0.7

        # Calculate Ribbon new size
        new_width = int(rack.width * rscale_factor)
        new_height = int(rack.height * rscale_factor)

        # Resize the rack
        rack = rack.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
        # Place the rack on the image
        bg.paste(rack, (rack_x, rack_y), mask=rack)   
        
        
    ##################################################################################
    # Marksman roles
    if mqual_roles:
        driverimg = Image.open("awards/Marksman.png")
        driverimg = driverimg.resize((100, 100), Image.Resampling.LANCZOS)
        bg.paste(driverimg, (mstart_x,mstart_y), mask=driverimg)
    # Loop through roles
    
    if mqual_roles:
        ribbon_width = 110
        ribbon_height = 35
        ribbons_per_row = 1
    
        ribbons = []
        for role in mqual_roles:
            role_name = role
            if role_name in mqual_templates:
                img_path = mqual_templates[role_name]
                img = Image.open(img_path)
                ribbons.append(img)
    
        if not ribbons:
            print("You don't have any marksman awards assigned to you")
        
        # Trim all ribbons first
        ribbons = [trim(ribbon) for ribbon in ribbons]
    
        # Count and calculate
        num_ribbons = len(ribbons)
        rows = (num_ribbons + ribbons_per_row - 1) // ribbons_per_row  # ceiling division
        rack_width = min(ribbons_per_row, num_ribbons) * ribbon_width
        rack_height = rows * ribbon_height
    
        # Create blank rack
        rack = Image.new('RGBA', (rack_width, rack_height), (255, 255, 255, 0))
    
        # Reverse ribbons for right-to-left, bottom-to-top stacking
        ribbons = list(reversed(ribbons))
    
        # Build the rack
        for index, ribbon in enumerate(ribbons):
            row = (rows - 1) - (index // ribbons_per_row)  # bottom up
            col = ribbons_per_row - 1 - (index % ribbons_per_row)  # right to left
    
            # Default x, y position
            x = col * ribbon_width
            y = row * ribbon_height - (row * 10)
    
            # Center the top row if incomplete
            if row == 0:
                ribbons_in_top_row = num_ribbons % ribbons_per_row
                if ribbons_in_top_row == 0:
                    ribbons_in_top_row = ribbons_per_row
    
                total_row_width = ribbons_in_top_row * ribbon_width
                offset = (rack_width - total_row_width) // 2
    
                x = (col - (ribbons_per_row - ribbons_in_top_row)) * ribbon_width + offset
            else:
                x = col * ribbon_width
                
            # Resize ribbon to fit exactly if needed
            ribbon = ribbon.resize((ribbon_width, ribbon_height))
    
            # Paste ribbon
            rack.paste(ribbon, (x, y), mask=ribbon if ribbon.mode == 'RGBA' else None)

        # Draw a black frame around the rack
        draw = ImageDraw.Draw(rack)
        draw.rectangle([(0, 0), (rack_width -1, rack_height -1)], outline="black", width=0)
    
        rackname = f"{member.name}_ribbons.png"
        rack.save(rackname)

        # Set Rack Location
        rack_x = mstart_x + 15 
        rack_y = mstart_y + 90

        # Ribbon Scale by a factor 
        rscale_factor = 0.7

        # Calculate Ribbon new size
        new_width = int(rack.width * rscale_factor)
        new_height = int(rack.height * rscale_factor)

        # Resize the rack
        rack = rack.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
        # Place the rack on the image
        bg.paste(rack, (rack_x, rack_y), mask=rack)
        
    #######################################################  
    # Save the picture with the all elements
    bg.save(filename_r)   
     
    # Send the file to discord
    await ctx.send(file=discord.File(filename_r))
    
    # Temp file cleanup
    os.remove(rackname)
    os.remove(filename)
    os.remove(filename_r)

# Run bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))

