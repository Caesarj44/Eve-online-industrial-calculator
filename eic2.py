import pandas as pd
import customtkinter as CTk
from CTkTable import *
import os
from typing_extensions import Self
from dataclasses import dataclass, field
import math
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
path = 'EOrec/'
path_to_export = 'output_excel/'

@dataclass
class  ingredient (): # можно ещё добавить свойство "достаточно ли в наличии" или же "ингридиент произведён", при котором ингридиент не учитывается
  name: str
  needed_quantity: int
  production_per_run: int = 1
  run_needed: int = 0
  price: int = 0

@dataclass
class ingredients_list():
  ingredients: list[ingredient] = field(default_factory=list)

@dataclass
class player_charachteristics(): #задел под будущее
  material_efficienty: int = 20
  time_efficienty: int = 10



ingredients_in_warehouse = ingredients_list()
for i in ingredients_in_warehouse.ingredients:
  ingredients_in_warehouse_names.append(i.name)


class EICsheet_frame(CTk.CTkScrollableFrame):
  def __init__(self,master, title,df):
    super().__init__(master)
    value = []
    self.v = ['index', 'name', 'needed quantity', 'runs need']
    self.v.extend(df.columns)
    value.append(self.v)
    for i, row in df.iterrows():
      value.append([i]+list(row))

    self.title = title
    self.grid_columnconfigure(0,weight=1)
    self.grid_rowconfigure(0, weight=1)
    self.table_sheet = CTkTable(self, row = len(value), column =4, values=value)
    self.table_sheet.grid(row=1, column=0, rowspan = 5)
    self.title = CTk.CTkLabel(self, text = self.title,)
    self.title.grid(row = 0,column = 0,columnspan = 3)

class App(CTk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600')
        self.title('EveIndCalc 2')
        self.resizable(width= 'FALSE', height= 'FALSE')

        self.pd_sheet = pd.DataFrame({
        })

        self.input_text_frame = CTk.CTkLabel(master = self,text = 'Bluprint:', width= 100, height= 20)
        self.input_text_frame.grid(row = 0, column = 0, padx=(10,20), pady =(10,20), sticky = "ew" )

        self.to_input_text_frame = CTk.CTkEntry(master = self, width= 200, height= 20, placeholder_text = 'What do you want?')
        self.to_input_text_frame.grid(row = 0, column = 1, padx=(10,20),pady =(10,20), sticky = "ew" )

        self.button_to_start = CTk.CTkButton(self, text ='Calculate', width = 50, height = 20, command = self.start_code_by_button)
        self.button_to_start.grid(row = 0, column = 2,padx=(10,20),pady =(10,20), sticky = "ew" )

        self.bibaboba = CTk.CTkButton(self,text = 'to Excel(.xlsx):', width= 100, height= 20,fg_color= 'Forest Green',hover_color= 'dark green', command = self.export_to_excel)
        self.bibaboba.grid(row = 0, column = 3, padx=(10,20), pady =(10,20), sticky = "ew" )

        self.sheetframe = EICsheet_frame(self, 'Bill',self.pd_sheet)
        self.sheetframe.grid(row = 2, column = 0, columnspan = 4,rowspan = 5, padx = (40,20), pady = (40,20), sticky="nsew")







        self.to_produce = str()
        self.common_ingredient_list = ingredients_list() #список со множеством всех ингридиентов, с повторениями
        self.total_ingredient_list = ingredients_list() #список со всеми ингридиентами, без повторений
        self.file_doesnt_exsist = list() # = nonconstructable_list
        self.already_producted = ingredients_list() #элемент добавляется сюда, если в наличии его больше, чем надо или если есть отметка что он уже произведёт(будет в будущем)
        self.ingredients_in_warehouse = ingredients_list()
        self.ingredients_in_warehouse_names = list()
        



    def create_pandas_file(self, list_to_pandas):
      intername = list()
      interneedquant = list()
      internedrun = list()
      for i in list_to_pandas.ingredients: #создаём pandas dataframe построчно
        intername.append(i.name)
        interneedquant.append(i.needed_quantity)
        internedrun.append(i.run_needed)
        dataframe = pd.DataFrame({
            'name':intername,
            'needed quantity':interneedquant,
            'runs needed':internedrun
        })
      
      self.pd_sheet = dataframe
      return(dataframe)
    
    def export_to_excel(self): #функция создания excel файла из pandas dataframe
      list_to_export = self.start_code_by_button()
      list_to_export.to_excel(path_to_export + self.to_calculate_input + '.xlsx')
    
    def start_code_by_button(self):
      self.to_calculate_input = self.to_input_text_frame.get()
      self.file_path = path + self.to_calculate_input + ".txt"
      path_to_file = self.file_path
      self.values_to_update = []
      if os.path.exists(path_to_file):
        self.first_list = self.read_recipe_file(path_to_file)
        self.second_list = self.next_list_generator(self.first_list, self.file_doesnt_exsist)
        self.third_list = self.next_list_generator(self.second_list, self.file_doesnt_exsist)
        self.fourth_list = self.next_list_generator(self.third_list, self.file_doesnt_exsist)
        self.fifth_list = self.next_list_generator(self.fourth_list, self.file_doesnt_exsist)
        self.all_list = [self.first_list,self.second_list,self.third_list,self.fourth_list, self.fifth_list]
        print(self.file_path)
        for i in self.all_list:
          for j in i.ingredients:
            self.common_ingredient_list.ingredients.append(j)
            self.total_ingredient_list = self.removing_duplicate_elements(self.common_ingredient_list)

        self.pd_sheet = self.create_pandas_file(self.total_ingredient_list)
        print(self.pd_sheet)

        for i in self.total_ingredient_list.ingredients:
          if not os.path.exists(path + i.name + '.txt') and i.name not in self.file_doesnt_exsist:
            self.file_doesnt_exsist.append(i.name)
        print('Рецепта не сущствует в папке!:', self.file_doesnt_exsist)
    
      else:
        print('needed recipt doesnt exist:',self.to_calculate_input, 'in this folder:',self.file_path)

      self.va = ['index'] #костыль обновления отображаемой таблицы
      self.va.extend(self.pd_sheet.columns)
      self.values_to_update.append(self.va)

      for i, row in self.pd_sheet.iterrows():
        self.values_to_update.append([i]+list(row))

      self.sheetframe.table_sheet.rows = len(self.total_ingredient_list.ingredients) + 2
      self.sheetframe.table_sheet.update_values(self.values_to_update)
      self.common_ingredient_list = ingredients_list() #список со множеством всех ингридиентов, с повторениями
      self.total_ingredient_list = ingredients_list() #список со всеми ингридиентами, без повторений
      self.file_doesnt_exsist = list() # = nonconstructable_list
      return(self.pd_sheet)
    
    def read_recipe_file(self,reciepe_file): #читает файл и возвращает список классов с указанием ингридиента рецепта и требуемого количества
      first_ingredient_list = ingredients_list()
      with open(reciepe_file) as reciept:
        product_quantity = (int(reciept.readline().strip())) #по-факту уже пропуск первой строчки
        for line in reciept:
          parts = line.split(",") #danger!No empty lines allowed
          ingredient_name = parts[0].strip() #part 1 before a comma
          #ingredient_quant = parts[1].strip() #часть 2 после запятой
          ingredient_name = ingredient(parts[0].strip(), int(parts[1].strip())) #создаём для каждой строчки свой класс, указывая имя и количество
          #ахахахаххахаха сука))0 первый баг. Если не указать тут int то получается str
          first_ingredient_list.ingredients.append(ingredient_name) # расщиряем список с ингредиентами
      return first_ingredient_list   
    
    def per_run(self,element): #функция, берёт ингридиент, открывает файл с его рецептом, смотрит сколько производится за раз(первая строчка) и записывает это в класс ингридиента
      if os.path.exists(path + element.name + '.txt'):
        with open(path + element.name + '.txt') as reciept:
          element.production_per_run = (int(reciept.readline().strip())) #читает первую строчку
      return(element)
    
    def next_list_generator(self, input_list, nonconstructable_list):# Функция для расчета ингридиентов в следующем уровне
      pre_output_list = ingredients_list()
      output_list = ingredients_list()
      for i in input_list.ingredients:
        i = self.per_run(i)
        if os.path.exists(path + i.name + '.txt'):
          if i.name in self.ingredients_in_warehouse_names:
            for k in ingredients_in_warehouse:
              if k.name == i.name:
                i.needed_quantity -= k.needed_quantity
          else:
            print(i.name)
            inter_list = self.read_recipe_file(path + i.name + '.txt') #список для каждого отдельного рецепта
            i.run_needed = math.ceil(i.needed_quantity / i.production_per_run)
            for j in inter_list.ingredients:
              #j.needed_quantity = math.ceil(j.needed_quantity * (i.needed_quantity / i.production_per_run))
              j.needed_quantity = math.ceil(j.needed_quantity * i.run_needed)
              #print(j.name, j.needed_quantity, j.production_per_run, i.run_needed)
              pre_output_list.ingredients.append(j)
        else:
          nonconstructable_list.append(i.name)
        #print('_'*3)
      output_list = self.removing_duplicate_elements(pre_output_list)
      #output_list = pre_output_list
      return(output_list)
    
    def removing_duplicate_elements(self, input_list): #функция, которая удаляет повторяющиеся элементы из списка, прибавляя к существующим needed_quantity
      output_list = ingredients_list()
      inter_name_list = list()
      for i in input_list.ingredients:
        if i.name not in inter_name_list:
          inter_name_list.append(i.name)
          output_list.ingredients.append(i)
        else:
          for j in output_list.ingredients:
            if i.name == j.name:
              j.needed_quantity += i.needed_quantity
      return(output_list)



      
if __name__ == '__main__':
    app = App()
    
    app.mainloop()






