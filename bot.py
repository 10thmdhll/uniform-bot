import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import os
import aiohttp
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# === Template definitions ===
rank_templates = {
    "Col.": {"Rank": "Colonel", "icon_position": (660,420)},
    "Lt. Col.": {"Rank": "Lieutenant Colonel", "icon_position": (660,420)},
    "CSM.": {"Rank": "Command Sergeant Major", "icon_position": (625,525)},
    "Maj.": {"Rank": "Major", "icon_position": (660,420)},
    "Cpt.": {"Rank": "Captain", "icon_position": (660,420)},
    "SGM.": {"Rank": "Sergeant Major", "icon_position": (625,525)},
    "1st Sgt.": {"Rank": "First Sergeant", "icon_position": (625,525)},
    "M/Sgt.": {"Rank": "Master Sergeant", "icon_position": (625,525)},
    "1Lt.": {"Rank": "First Lieutenant", "icon_position": (660,420)},
    "CWO.": {"Rank": "Chief Warrant Officer", "icon_position": (660,420)},
    "2Lt.": {"Rank": "Second Lieutenant", "icon_position": (660,420)},
    "T/Sgt.": {"Rank": "Technical Sergeant", "icon_position": (625,525)},
    "WO.": {"Rank": "Warrant Officer", "icon_position": (660,420)},
    "S/Sgt.": {"Rank": "Staff Sergeant", "icon_position": (625,525)},
    "Sgt.": {"Rank": "Sergeant", "icon_position": (625,525)},
    "Cpl.": {"Rank": "Corporal", "icon_position": (625,525)},
    "T/3": {"Rank": "Technician Third Grade", "icon_position": (625,525)},
    "T/4": {"Rank": "Technician Fourth Grade", "icon_position": (625,525)},
    "T/5": {"Rank": "Technician Fifth Grade", "icon_position": (625,525)},
    "Pfc.": {"Rank": "Private First Class", "icon_position": (625,525)},
    "Pvt.": {"Rank": "Private", "icon_position": (625,525)}
}
assignment_templates = {
    "Division Command": {"Assignment": "Division Command", "icon_position": (100,600)},
    "Battalion Leadership": {"Assignment": "Battalion Command", "icon_position": (100,600)},
    "Fox Company Leadership": {"Assignment": "Fox Company Command", "icon_position": (100,600)},
    "FP1 - Leadership": {"Assignment": "Fox Company First Platoon Command", "icon_position": (100,600)},
    "FP2 - Leadership": {"Assignment": "Fox Company Second Platoon Command", "icon_position": (100,600)},
    "FP3 - Leadership": {"Assignment": "Fox Company Third Platoon Command", "icon_position": (100,600)},
    "FP1S1": {"Assignment": "Fox Company First Platoon First Squad", "icon_position": (100,600)},
    "FP1S2": {"Assignment": "Fox Company First Platoon Second Squad", "icon_position": (100,600)},
    "FP1S3": {"Assignment": "Fox Company First Platoon Third Squad", "icon_position": (100,600)},
    "FP1S4": {"Assignment": "Fox Company First Platoon Fourth Squad", "icon_position": (100,600)},
    "FP2S1": {"Assignment": "Fox Company Second Platoon First Squad", "icon_position": (100,600)},
    "FP2S2": {"Assignment": "Fox Company Second Platoon Second Squad", "icon_position": (100,600)},
    "FP2S3": {"Assignment": "Fox Company Second Platoon Third Squad", "icon_position": (100,600)},
    "FP2S4": {"Assignment": "Fox Company Second Platoon Fourth Squad", "icon_position": (100,600)},
    "FP3S1": {"Assignment": "Fox Company Third Platoon First Squad", "icon_position": (100,600)},
    "FP3S2": {"Assignment": "Fox Company Third Platoon Second Squad", "icon_position": (100,600)},
    "FP3S3": {"Assignment": "Fox Company Third Platoon Third Squad", "icon_position": (100,600)},
    "FP3S4": {"Assignment": "Fox Company Third Platoon Fourth Squad", "icon_position": (100,600)}
}
award_templates = {
    "Founders Silver Ribbon": {"Award": "Founders Silver Ribbon", "icon_position": (980,480)},
    "Founders Ribbon": {"Award": "Founders Ribbon", "icon_position": (980,480)},
    "Distinguished Service Cross": {"Award": "Distinguished Service Cross", "icon_position": (1030,480)},
    "Distinguished Service Medal": {"Award": "Distinguished Service Medal", "icon_position": (980,500)},
    "Silver Star": {"Award": "Silver Star", "icon_position": (1030,500)},
    "Bronze Star - 10": {"Award": "Bronze Star - 10", "icon_position": (980,520)},
    "Bronze Star - 9": {"Award": "Bronze Star - 9", "icon_position": (980,520)},
    "Bronze Star - 8": {"Award": "Bronze Star - 8", "icon_position": (980,520)},
    "Bronze Star - 7": {"Award": "Bronze Star - 7", "icon_position": (980,520)},
    "Bronze Star - 6": {"Award": "Bronze Star - 6", "icon_position": (980,520)},
    "Bronze Star - 5": {"Award": "Bronze Star - 5", "icon_position": (980,520)},
    "Bronze Star - 4": {"Award": "Bronze Star - 4", "icon_position": (980,520)},
    "Bronze Star - 3": {"Award": "Bronze Star - 3", "icon_position": (980,520)},
    "Bronze Star - 2": {"Award": "Bronze Star - 2", "icon_position": (980,520)},
    "Bronze Star - 1": {"Award": "Bronze Star - 1", "icon_position": (980,520)},
    "Purple Heart - 10": {"Award": "Purple Heart - 10", "icon_position": (1030,520)},
    "Purple Heart - 9": {"Award": "Purple Heart - 9", "icon_position": (1030,520)},
    "Purple Heart - 8": {"Award": "Purple Heart - 8", "icon_position": (1030,520)},
    "Purple Heart - 7": {"Award": "Purple Heart - 7", "icon_position": (1030,520)},
    "Purple Heart - 6": {"Award": "Purple Heart - 6", "icon_position": (1030,520)},
    "Purple Heart - 5": {"Award": "Purple Heart - 5", "icon_position": (1030,520)},
    "Purple Heart - 4": {"Award": "Purple Heart - 4", "icon_position": (1030,520)},
    "Purple Heart - 3": {"Award": "Purple Heart - 3", "icon_position": (1030,520)},
    "Purple Heart - 2": {"Award": "Purple Heart - 2", "icon_position": (1030,520)},
    "Purple Heart - 1": {"Award": "Purple Heart - 1", "icon_position": (1030,520)},
    "Meritorious Service Medal - 5": {"Award": "Meritorious Service Medal - 5", "icon_position": (930,540)},
    "Meritorious Service Medal - 4": {"Award": "Meritorious Service Medal - 4", "icon_position": (930,540)},
    "Meritorious Service Medal - 3": {"Award": "Meritorious Service Medal - 3", "icon_position": (930,540)},
    "Meritorious Service Medal - 2": {"Award": "Meritorious Service Medal - 2", "icon_position": (930,540)},
    "Meritorious Service Medal - 1": {"Award": "Meritorious Service Medal - 1", "icon_position": (930,540)},
    "Army Commendation Medal - 10": {"Award": "Army Commendation Medal - 10", "icon_position": (980,540)},
    "Army Commendation Medal - 9": {"Award": "Army Commendation Medal - 9", "icon_position": (980,540)},
    "Army Commendation Medal - 8": {"Award": "Army Commendation Medal - 8", "icon_position": (980,540)},
    "Army Commendation Medal - 7": {"Award": "Army Commendation Medal - 7", "icon_position": (980,540)},
    "Army Commendation Medal - 6": {"Award": "Army Commendation Medal - 6", "icon_position": (980,540)},
    "Army Commendation Medal - 5": {"Award": "Army Commendation Medal - 5", "icon_position": (980,540)},
    "Army Commendation Medal - 4": {"Award": "Army Commendation Medal - 4", "icon_position": (980,540)},
    "Army Commendation Medal - 3": {"Award": "Army Commendation Medal - 3", "icon_position": (980,540)},
    "Army Commendation Medal - 2": {"Award": "Army Commendation Medal - 2", "icon_position": (980,540)},
    "Army Commendation Medal - 1": {"Award": "Army Commendation Medal - 1", "icon_position": (980,540)},
    "Army Achievement Medal - 10": {"Award": "Army Achievement Medal - 10", "icon_position": (1030,540)},
    "Army Achievement Medal - 9": {"Award": "Army Achievement Medal - 9", "icon_position": (1030,540)},
    "Army Achievement Medal - 8": {"Award": "Army Achievement Medal - 8", "icon_position": (1030,540)},
    "Army Achievement Medal - 7": {"Award": "Army Achievement Medal - 7", "icon_position": (1030,540)},
    "Army Achievement Medal - 6": {"Award": "Army Achievement Medal - 6", "icon_position": (1030,540)},
    "Army Achievement Medal - 5": {"Award": "Army Achievement Medal - 5", "icon_position": (1030,540)},
    "Army Achievement Medal - 4": {"Award": "Army Achievement Medal - 4", "icon_position": (1030,540)},
    "Army Achievement Medal - 3": {"Award": "Army Achievement Medal - 3", "icon_position": (1030,540)},
    "Army Achievement Medal - 2": {"Award": "Army Achievement Medal - 2", "icon_position": (1030,540)},
    "Army Achievement Medal - 1": {"Award": "Army Achievement Medal - 1", "icon_position": (1030,540)},
    "Army Good Conduct Medal - 10": {"Award": "Army Good Conduct Medal - 10", "icon_position": (930,560)},
    "Army Good Conduct Medal - 9": {"Award": "Army Good Conduct Medal - 9", "icon_position": (930,560)},
    "Army Good Conduct Medal - 8": {"Award": "Army Good Conduct Medal - 8", "icon_position": (930,560)},
    "Army Good Conduct Medal - 7": {"Award": "Army Good Conduct Medal - 7", "icon_position": (930,560)},
    "Army Good Conduct Medal - 6": {"Award": "Army Good Conduct Medal - 6", "icon_position": (930,560)},
    "Army Good Conduct Medal - 5": {"Award": "Army Good Conduct Medal - 5", "icon_position": (930,560)},
    "Army Good Conduct Medal - 4": {"Award": "Army Good Conduct Medal - 4", "icon_position": (930,560)},
    "Army Good Conduct Medal - 3": {"Award": "Army Good Conduct Medal - 3", "icon_position": (930,560)},
    "Army Good Conduct Medal - 2": {"Award": "Army Good Conduct Medal - 2", "icon_position": (930,560)},
    "Army Good Conduct Medal - 1": {"Award": "Army Good Conduct Medal - 1", "icon_position": (930,560)},
    "American Defense Service Medal": {"Award": "American Defense Service Medal", "icon_position": (980,560)},
    "Army Service Ribbon": {"Award": "Army Service Ribbon", "icon_position": (1030,600)},
    "American Campaign Medal - 5": {"Award": "American Campaign Medal - 5", "icon_position": (1030,580)},
    "American Campaign Medal - 4": {"Award": "American Campaign Medal - 4", "icon_position": (1030,580)},
    "American Campaign Medal - 3": {"Award": "American Campaign Medal - 3", "icon_position": (1030,580)},
    "American Campaign Medal - 2": {"Award": "American Campaign Medal - 2", "icon_position": (1030,580)},
    "American Campaign Medal - 1": {"Award": "American Campaign Medal - 1", "icon_position": (1030,580)},
    "World War II Victory Medal": {"Award": "World War II Victory Medal", "icon_position": (930,580)},
    "Gold Lifesaving Medal": {"Award": "Gold Lifesaving Medal", "icon_position": (930,620)},
    "Silver Lifesaving Medal": {"Award": "Silver Lifesaving Medal", "icon_position": (1030,620)},
    "Medal of Humane Action": {"Award": "Medal of Humane Action", "icon_position": (1030,580)},
    "Army of Occupation Medal": {"Award": "Army of Occupation Medal", "icon_position": (980,580)},
    "Armed Forces Service Medal": {"Award": "Armed Forces Service Medal", "icon_position": (930,600)},
    "Combat Infantryman Badge": {"Award": "Combat Infantryman Badge", "icon_position": (1000,440)},
    "Expert Infantryman Badge": {"Award": "Expert Infantryman Badge", "icon_position": (1000,440)},
    "NCO Development Ribbon - Infantry": {"Award": "NCO Development Ribbon - Infantry", "icon_position": (980,600)},
    "NCO Development Ribbon - Armor": {"Award": "NCO Development Ribbon - Armor", "icon_position": (980,620)},
    "ReClimb Unit Commendation": {"Award": "ReClimb Unit Commendation", "icon_position": (735,590)},
    "Ranger": {"Award": "Ranger", "icon_position": (1110,440)},
    "Recon": {"Award": "Recon", "icon_position": (1110,460)},
    "Pathfinder": {"Award": "Pathfinder", "icon_position": (1110,480)},
    "Driver - Tank Weapons": {"Award": "Driver - Tank Weapons", "icon_position": (800,825)},
    "Driver - Tracked": {"Award": "Driver - Tracked", "icon_position": (900,825)},
    "Driver - Wheeled": {"Award": "Driver - Wheeled", "icon_position": (1000,825)},
    "Driver - Mechanic": {"Award": "Driver - Mechanic", "icon_position": (1100,825)},
    "Expert - Artillery": {"Award": "Expert - Artillery", "icon_position": (800,950)},
    "Expert - Anti Tank": {"Award": "Expert - Anti Tank", "icon_position": (900,950)},
    "Expert - Auto Rifle": {"Award": "Expert - Auto Rifle", "icon_position": (1000,950)},
    "Expert - Grenade": {"Award": "Expert - Grenade", "icon_position": (1100,950)},
    "Expert - MG": {"Award": "Expert - MG", "icon_position": (700,1075)},
    "Expert - Pistol": {"Award": "Expert - Pistol", "icon_position": (800,1075)},
    "Expert - Rifle": {"Award": "Expert - Rifle", "icon_position": (900,1075)},
    "Expert - Scoped Rifle": {"Award": "Expert - Scoped Rifle", "icon_position": (1000,1075)},
    "Expert - SMG": {"Award": "Expert - SMG", "icon_position": (1100,1075)},
    "Sharpshooter - Artillery": {"Award": "Sharpshooter - Artillery", "icon_position": (800,950)},
    "Sharpshooter - Anti Tank": {"Award": "Sharpshooter - Anti Tank", "icon_position": (900,950)},
    "Sharpshooter - Auto Rifle": {"Award": "Sharpshooter - Auto Rifle", "icon_position": (1000,950)},
    "Sharpshooter - Grenade": {"Award": "Sharpshooter - Grenade", "icon_position": (1100,950)},
    "Sharpshooter - MG": {"Award": "Sharpshooter - MG", "icon_position": (700,1075)},
    "Sharpshooter - Pistol": {"Award": "Sharpshooter - Pistol", "icon_position": (800,1075)},
    "Sharpshooter - Rifle": {"Award": "Sharpshooter - Rifle", "icon_position": (900,1075)},
    "Sharpshooter - Scoped Rifle": {"Award": "Sharpshooter - Scoped Rifle", "icon_position": (1000,1075)},
    "Sharpshooter - SMG": {"Award": "Sharpshooter - SMG", "icon_position": (1100,1075)},
    "Marksman - Artillery": {"Award": "Marksman - Artillery", "icon_position": (800,950)},
    "Marksman - Anti Tank": {"Award": "Marksman - Anti Tank", "icon_position": (900,950)},
    "Marksman - Auto Rifle": {"Award": "Marksman - Auto Rifle", "icon_position": (1000,950)},
    "Marksman - Grenade": {"Award": "Marksman - Grenade", "icon_position": (1100,950)},
    "Marksman - MG": {"Award": "Marksman - MG", "icon_position": (700,1075)},
    "Marksman - Pistol": {"Award": "Marksman - Pistol", "icon_position": (800,1075)},
    "Marksman - Rifle": {"Award": "Marksman - Rifle", "icon_position": (900,1075)},
    "Marksman - Scoped Rifle": {"Award": "Marksman - Scoped Rifle", "icon_position": (1000,1075)},
    "Marksman - SMG": {"Award": "Marksman - SMG", "icon_position": (1100,1075)}
}

# === Utility: download role icon with caching ===
async def download_role_icon(role):
    if role.icon:
        fname = f"role_icon_{role.id}.png"
        if not os.path.exists(fname):
            async with aiohttp.ClientSession() as session:
                async with session.get(role.icon.url) as resp:
                    if resp.status == 200:
                        with open(fname, 'wb') as f:
                            f.write(await resp.read())
        return fname
    return None

# === Generate uniform card image ===
def generate_uniform_card(user_name, rank_role, rank_data, assign_role, assign_data, award_roles, role_icons, filename):
    width, height = 1200, 1200
    img = Image.new("RGB", (width, height), color=(34, 45, 30))
    draw = ImageDraw.Draw(img)

    # Draw background silhouette first so icons appear on top
    sil_path = "Infantry.png"
    if os.path.exists(sil_path):
        try:
            sil = Image.open(sil_path).resize((600, 800))
            img.paste(sil, (600, 380), sil.convert("RGBA"))
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
    if rank_role and rank_data:
        # Draw rank text
        rank_value = rank_data.get("Rank", "")
        draw.text((40, y), f"Rank: {rank_value}", fill="white", font=text_font)
        y += 40
        # Draw rank icon if exists
        shoulder_list = ["Colonel", "Lieutenant Colonel", "Major", "Captain", "Chief Warrant Officer", "Warrant Officer","First Lieutenant", "Second Lieutenant"]
        icon_path = role_icons.get(rank_role)
        icon_pos = rank_data.get("icon_position", (20, y))
        if icon_path and os.path.exists(icon_path):
            if rank_value in shoulder_list:
                icon_img = Image.open(icon_path).resize((40, 40))
            else:
                icon_img = Image.open(icon_path).resize((80, 80))
                
            img.paste(icon_img, icon_pos, icon_img.convert("RGBA"))

    # Assignment section
    if assign_role and assign_data:
        y += 60
        assign_value = assign_data.get("Assignment", "")
        draw.text((40, y), f"Assignment: {assign_value}", fill="white", font=text_font)
        # Draw assignment icon
        icon_path = role_icons.get(assign_role)
        icon_pos = assign_data.get("icon_position", (20, y))
        if icon_path and os.path.exists(icon_path):
            icon_img = Image.open(icon_path).resize((40, 40))
            img.paste(icon_img, icon_pos, icon_img.convert("RGBA"))
        y += 40

    # Awards (other roles) section
    y += 60
    draw.text((40, y), "Awards:", fill="white", font=text_font)
    y += 40
    
    # List award names below icons
    list_y = y
    for aw in award_roles:
        draw.text((40, list_y), f"- {aw}", fill="white", font=small_font)
        list_y += 30
    
    large_awards = ["Driver - Tank Weapons", "Driver - Tracked", "Driver - Wheeled", "Driver - Mechanic"
        , "Marksman - Artillery","Marksman - Anti Tank", "Marksman - Auto Rifle", "Marksman - Grenade", "Marksman - MG"
        , "Marksman - Pistol", "Marksman - Rifle", "Marksman - Scoped Rifle", "Marksman - SMG"
        , "Sharpshooter - Artillery", "Sharpshooter - Anti Tank", "Sharpshooter - Auto Rifle", "Sharpshooter - Grenade", "Sharpshooter - MG"
        , "Sharpshooter - Pistol", "Sharpshooter - Rifle", "Sharpshooter - Scoped Rifle", "Sharpshooter - SMG"
        , "Expert - Artillery", "Expert - Anti Tank", "Expert - Auto Rifle", "Expert - Grenade", "Expert - MG"
        , "Expert - Pistol", "Expert - Rifle", "Expert - Scoped Rifle", "Expert - SMG"        
        ]
        
    double_length_awards = ["Combat Infantryman Badge","Expert Infantryman Badge"]
    
    for aw in award_roles:
        # Draw award icon
        icon_path = role_icons.get(aw)
        icon_pos = award_templates.get(aw, {}).get("icon_position", (20, y))
        if icon_path and os.path.exists(icon_path):
            if aw in large_awards:
                icon_img = Image.open(icon_path).resize((100, 80))
            
            else:
                if aw in double_length_awards:
                    icon_img = Image.open(icon_path).resize((100, 40))
                
                else:
                    icon_img = Image.open(icon_path).resize((50, 20))
                
        img.paste(icon_img, icon_pos, icon_img.convert("RGBA"))
        
        y += 40
        
    # Save final image
    img.save(filename)

# === Bot setup ===
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command()
async def uniform(ctx):
    member = ctx.author
    # Gather all roles except @everyone
    all_roles = sorted([r for r in member.roles if r.name != "@everyone"], key=lambda r: r.position)

    # Determine primary rank and assignment
    template_roles = [r for r in reversed(all_roles) if r.name in rank_templates]
    rank_role = template_roles[0].name if template_roles else None
    rank_data = rank_templates.get(rank_role, {}) if rank_role else {}

    assign_roles = [r for r in reversed(all_roles) if r.name in assignment_templates]
    assign_role = assign_roles[0].name if assign_roles else None
    assign_data = assignment_templates.get(assign_role, {}) if assign_role else {}

    # Other roles
    award_roles = [r.name for r in reversed(all_roles) if r.name in award_templates]

    # Download icons
    role_icons = {}
    for r in member.roles:
        path = await download_role_icon(r)
        if path:
            role_icons[r.name] = path

    # Generate and send image
    filename = f"{member.display_name}_uniform.png"
    generate_uniform_card(
        member.display_name,
        rank_role,
        rank_data,
        assign_role,
        assign_data,
        award_roles,
        role_icons,
        filename
    )
    await ctx.send(file=discord.File(filename))
    os.remove(filename)

# Run bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))

