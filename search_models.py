import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
import tkinter.font as tkFont
import threading
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys


def InfiniteScrolling(driver):
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(4)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height



def Cairo_Sales_Web(driver,list_of_categories,data,Sharaf_DG):
        output_df = pd.DataFrame(columns=['Model','Cairo_Sales'])
        for cate in list_of_categories:
            df = data[data['Category'] == cate]
            # print(df)
            list_of_models = df["Models"]
            # We got the models of one category
            check_once = 0
            for models in list_of_models:

                driver.get("https://cairosales.com/en/find?search_query="+models)
                try:
                    ids=  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-count"))).text
                    time.sleep(5)
                    if "Showing 1 - 1 of".lower() in ids.lower():
                        product_link = driver.find_element(By.CSS_SELECTOR,".product_img_link").get_attribute("href")
                        print(product_link)
                        output_df = output_df.append({
                                    "Model":models,
                                    "Cairo_Sales": "o",
                                    "links": product_link
                            },ignore_index=True)
                        print(models,"Found")
                    else:
                        output_df = output_df.append({
                                    "Model":models,
                                    "Cairo_Sales": "x",
                                    "links": ""
                            },ignore_index=True)
                        print(models,"Not Found")
                        pass
                except:
                    output_df = output_df.append({
                            "Model":models,
                            "Cairo_Sales": "x",
                            "links": ""
      
                    },ignore_index=True)
                    print(models,"Not Found")
               

        with pd.ExcelWriter("output.xlsx",mode="a",if_sheet_exists='replace') as writer:
            output_df.to_excel(writer,sheet_name="Cairo_Sales")
        
def Btech_Web(driver,list_of_categories,data,Sharaf_DG):
        output_df = pd.DataFrame(columns=['Model','BTech'])
        for cate in list_of_categories:
            df = data[data['Category'] == cate]
            # print(df)
            list_of_models = df["Models"]
            # We got the models of one category
            check_once = 0
            for models in list_of_models:
                if check_once == 0:
                    print("Model: ",models)
                    df_link = Sharaf_DG[Sharaf_DG['Category'] == cate]
                    keyword = models
                    # print(df_link["Links"])
                    dyno_link = df_link["Links"].iloc[0]
                    # print(dyno_link)
           
                    model_ids :list = []
                    driver.get(dyno_link)
                    # # Get scroll height
                    # InfiniteScrolling(driver)
                    
                    # driver.get(dyno_link)
                    time.sleep(5)
                    all_divs  = driver.find_elements(By.CSS_SELECTOR, ".product-item-view")
    
                    print(len(all_divs))
                    
                    while len(all_divs) < 100:
                        try:
                            element = driver.find_element(By.XPATH,"//div[@class='amscroll-load-button btn-outline primary medium']")
                            # Click the element
                            action = ActionChains(driver)
                            for i in range(0,7):
                                action.send_keys(Keys.UP).perform() 

                            time.sleep(10)
                            
                            action.move_to_element(element).click().perform()
                            
                            print("Clicked button")
                            time.sleep(10)
                            # element.click()
                            all_divs  = driver.find_elements(By.CSS_SELECTOR, ".product-item-view")

                        except:
                            print("Its breaking")
                            # time.sleep(15)
                            break
                        all_divs  = driver.find_elements(By.CSS_SELECTOR, ".product-item-view")
                        # print(len(all_divs))
                    counter = 0
                    # print(len(all_divs))
                    # Compare product name with model name 
                    for div in all_divs:
                        model_id = div.text
                        print(model_id)
                        check_once = 1
                        # Save this model id in the list and use it later 
                        # 
                        model_ids.append(model_id)



                total_models = len(model_ids)
                counter = 0
                for each_model in model_ids: 
                    if each_model.upper().find(models) != -1:
                        output_df = output_df.append({
                                "Model":models,
                                "Btech": "o",
                        },ignore_index=True)
                        print(models,"Found")
                        break
                    counter+=1

                if counter == total_models:
                    output_df = output_df.append({
                            "Model":models,
                            "Btech": "x",
      
                    },ignore_index=True)
                    print(models,"Not Found")
                
                # Compare here now

        with pd.ExcelWriter("output.xlsx",mode="a",if_sheet_exists='replace') as writer:
            output_df.to_excel(writer,sheet_name="Btech")
 

def Run_Cairo_Sales():




    # 0------------------------------------------------------------------------------
 
    data = pd.read_excel("models.xlsx",sheet_name="Models")
    Sharaf_DG = pd.read_excel("models.xlsx",sheet_name="Cairo_Sales")
   
    
    
    driver = webdriver.Chrome()
    list_of_categories = data["Category"].unique()

    Cairo_Sales_Web(driver,list_of_categories,data,Sharaf_DG)
    
  

def Run_Btech():

    data = pd.read_excel("models.xlsx",sheet_name="Models")
    Sharaf_DG = pd.read_excel("models.xlsx",sheet_name="Btech")

    driver = webdriver.Chrome()
    list_of_categories = data["Category"].unique()

    Btech_Web(driver,list_of_categories,data,Sharaf_DG)
 
        

# Main App 
class App:

    def __init__(self, root):
        #setting title
        root.title("Egypt Model Check")
        ft = tkFont.Font(family='Arial Narrow',size=13)
        #setting window size
        width=640
        height=480
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        root.configure(bg='black')

        ClickBtnLabel=tk.Label(root)
       
      
        
        ClickBtnLabel["font"] = ft
        
        ClickBtnLabel["justify"] = "center"
        ClickBtnLabel["text"] = "Egypt Model Check"
        ClickBtnLabel["bg"] = "black"
        ClickBtnLabel["fg"] = "white"
        ClickBtnLabel.place(x=120,y=190,width=150,height=70)
    

        
        Lulu=tk.Button(root)
        Lulu["anchor"] = "center"
        Lulu["bg"] = "#009841"
        Lulu["borderwidth"] = "0px"
        
        Lulu["font"] = ft
        Lulu["fg"] = "#ffffff"
        Lulu["justify"] = "center"
        Lulu["text"] = "START"
        Lulu["relief"] = "raised"
        Lulu.place(x=375,y=190,width=150,height=70)
        Lulu["command"] = self.start_func




  

    def ClickRun(self):

        running_actions = [
            Run_Cairo_Sales,          
            # Run_Btech,

        ]

        thread_list = [threading.Thread(target=func) for func in running_actions]

        # start all the threads
        for thread in thread_list:
            thread.start()

        # wait for all the threads to complete
        for thread in thread_list:
            thread.join()
    
    def start_func(self):
        thread = threading.Thread(target=self.ClickRun)
        thread.start()

    
        

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()


# Run()
