from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
import time
import json


driver = webdriver.Chrome()

stats_list =[]

try:
    driver.get("https://ru.dotabuff.com/heroes/meta")
    time.sleep(3)   
    
    soup = BeautifulSoup(driver.page_source, "html.parser")

    heroes_stats = soup.find("article", class_="r-tabbed-table").find_all("tr")
   
    for stats in heroes_stats:
        time.sleep(0.5)
        print("_"*100)
        heroes_names = stats.find("a", class_="link-type-hero")
        
        try:
            if heroes_names:
                names = heroes_names.text.strip()
                print(names)
        except Exception as e:
            print(f"Heroes name not found: {e}")
        
        try:
            first3medals_pickrates = stats.find("td", class_="r-tab r-group-1 cell-divider cell-strong sorted shown") or \
                                    stats.find("td", class_="r-tab r-group-1 cell-divider sorted shown")
            print("Herald, Guardian, Crusader:")
            if first3medals_pickrates:
                h_g_c_picks = first3medals_pickrates.text.strip()
                print(f"Pickrates: {h_g_c_picks}")
            first3medal_winrates = stats.find("td", class_="r-tab r-group-1 shown")
            if first3medal_winrates:
                h_g_c_wins = first3medal_winrates.text.strip()
                print(f"Winrates: {h_g_c_wins}")
        except Exception as e:
            print(f"Information about Heralds, Guardians, Crusaiders not found: {e}")
        
        try:
            archon_pikrates = stats.find("td", class_="r-tab r-group-2 cell-divider")
            print("Archon:")
            if archon_pikrates:
                archon_picks = archon_pikrates.text.strip()
                print(f"Pickrates: {archon_picks}")
            archon_winrates = stats.find("td", class_="r-tab r-group-2")
            if archon_winrates:
                archon_wins = archon_winrates.text.strip()
                print(f"Winrates: {archon_wins}")
        except Exception as e:
            print(f"Information about Archonts not found: {e}")
        
        try:
            legend_pickrates = stats.find("td", class_="r-tab r-group-3 cell-divider")
            print("Legend:")
            if legend_pickrates:
                legend_picks = legend_pickrates.text.strip()
                print(f"Pickrates: {legend_picks}")
            legend_winrates = stats.find("td", class_="r-tab r-group-3")
            if legend_winrates:
                legend_wins = legend_winrates.text.strip()
                print(f"Winrates: {legend_wins}")
        except Exception as e:
            print(f"Information about Legends not found: {e}")
        
        try:
            ancient_pickrates = stats.find("td", class_="r-tab r-group-4 cell-divider")
            print("Ancient:")
            if ancient_pickrates:
                anchient_picks = ancient_pickrates.text.strip()
                print(f"Pickrates: {anchient_picks}") 
            ancient_winrates = stats.find("td", class_="r-tab r-group-4")
            if ancient_winrates:
                anchient_wins = ancient_winrates.text.strip()
                print(f"Winrates: {anchient_wins}")
        except Exception as e:
            print(f"Information about Ancients not found: {e}")
        
        try:
            divine_immortal_pickrates = stats.find("td", class_="r-tab r-group-5 cell-divider")
            print("Divine, Immortal:")
            if divine_immortal_pickrates:
                d_i_picks = divine_immortal_pickrates.text.strip()
                print(f"Pickrates: {d_i_picks}")
            divine_immortal_winrates = stats.find("td", class_="r-tab r-group-5")
            if divine_immortal_winrates:
               d_i_wins = divine_immortal_winrates.text.strip()
               print(f"Winrates: {d_i_wins}")
        except Exception as e:
            print(f"Information about Divines and Immortals not found: {e}")

        try:
            stats_list.append({
                "Name": names,
                "Herald|Guardian|Crusaider Pickrates": h_g_c_picks,"Herald|Guardian|Crusaider Winrates": h_g_c_wins,
                "Archon Pickrate": archon_picks, "Archon Winrate": archon_wins,
                "Legend Pickrate": legend_picks, "Legend Winrate": legend_wins,
                "Ancient Pickrate": anchient_picks, "Ancient Winrate": anchient_wins,
                "Divine|Immortal Pickrate": d_i_picks, "Divine|Immortal Winrate": d_i_wins
            })
        except Exception as e:
            print(f"Couldn't add it to the list: {e}")

finally:
    driver.quit()

output_file = "dotabuff_pars.json"

try:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(stats_list, file, ensure_ascii=False, indent=4)
        print(f"The stats is saved to a file: {output_file}")

except Exception as e:
    print(f"Error writing file: {e}")