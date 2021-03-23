__author__ = "Theresa De Ocampo"
__version__ = "3.8.2"
__email__ = "maria.theresa.g.de.ocampo@gmail.com"

from tkinter import *
from matplotlib import pyplot as plt


class Statistics:
    def __init__(self, population, male, female, youth, young_adult, adult, senior, unemployed, employed, educ_tally):
        self.population = population
        self.male = male
        self.female = female
        self.youth = youth
        self.young_adult = young_adult
        self.adult = adult
        self.senior = senior
        self.unemployed = unemployed
        self.employed = employed
        self.educ_tally = educ_tally

        root = Tk()
        root.title("Analysis")
        root.config(bg="beige")
        root.resizable(False, False)  # Helps to disable windows from resizing

        window_height = 500
        window_width = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        # *******************************************   Frames   ******************************************* #
        main_frame = Frame(root, bg="beige", padx=10, pady=20)
        main_frame.pack()

        population_frame = Frame(main_frame, bg="teal", bd=3, relief=SOLID, width=550, height=150)
        population_frame.grid(row=0, column=0, columnspan=2)
        population_label = Label(population_frame, bg="teal", fg="white", font=("Glacial Indifference", 20, 'bold'),
                                 text="Total Registered Population", padx=10)
        population_label.pack(side=TOP)
        population_value = Label(population_frame, bg="teal", fg="white", font=("Glacial Indifference", 30, 'bold'),
                                 text=self.population, padx=10)
        population_value.pack(side=BOTTOM)

        gender_frame = Frame(main_frame, bg="beige", pady=10)
        gender_frame.grid(row=1, column=0, columnspan=2)
        male_frame = Frame(gender_frame, bg="teal", bd=3, relief=SOLID, width=270, height=150)
        male_frame.grid(row=0, column=0)
        male_frame.pack_propagate(False)
        male_label = Label(male_frame, bg="teal", fg="white", font=("Glacial Indifference", 20, 'bold'), text=" Male ",
                           padx=10)
        male_label.pack(side=TOP)
        male_value = Label(male_frame, bg="teal", fg="white", font=("Glacial Indifference", 30, 'bold'), text=self.male,
                           padx=10)
        male_value.pack(side=BOTTOM)

        seperator_frame = Frame(gender_frame, width=10)
        seperator_frame.grid(row=0, column=1)
        female_frame = Frame(gender_frame, bg="teal", bd=3, relief=SOLID, width=270, height=150)
        female_frame.grid(row=0, column=2)
        female_frame.pack_propagate(False)
        female_label = Label(female_frame, bg="teal", fg="white", font=("Glacial Indifference", 20, 'bold'),
                             text="Female", padx=10)
        female_label.pack(side=TOP)
        female_value = Label(female_frame, bg="teal", fg="white", font=("Glacial Indifference", 30, 'bold'),
                             text=self.female, padx=10)
        female_value.pack(side=BOTTOM)

        # *******************************************   Buttons   ******************************************* #
        age_button = Button(main_frame, text="Age Groups", font=("Glacial Indifference", 15, 'bold'), bd=5, width=15,
                            bg="light blue2", command=self.plot_age_groups)
        age_button.grid(row=2, column=0)

        occupation_button = Button(main_frame, text="Economic Status", font=("Glacial Indifference", 15, 'bold'), bd=5,
                                   width=15, bg="light blue2", command=self.plot_occupation)
        occupation_button.grid(row=2, column=1)

        seperator_buttons = Frame(main_frame, height=10)
        seperator_buttons.grid(row=3, column=0)

        education_button = Button(main_frame, text="Education Status", font=("Glacial Indifference", 15, 'bold'), bd=5,
                                  width=31, bg="light blue2", command=self.plot_education)
        education_button.grid(row=4, column=0, columnspan=2)

    def plot_age_groups(self):
        plt.style.use("fivethirtyeight")
        slices = [self.youth, self.young_adult, self.adult, self.senior]
        labels = ["Youth (< 18)", "Young Adult (18 to 35)", "Adult (36 to 55)", "Senior (> 56)"]
        explode = [0, 0, 0.1, 0]

        plt.pie(slices, labels=labels, explode=explode, shadow=True, startangle=90, autopct='%1.1f%%',
                wedgeprops={'edgecolor': 'black'})
        plt.title("Age Groups")
        plt.tight_layout()
        plt.show()

    def plot_occupation(self):
        plt.style.use("fivethirtyeight")
        slices = [self.unemployed, self.employed]
        labels = ['Unemployed', 'Employed']

        plt.pie(slices, labels=labels, shadow=True, startangle=90, autopct='%1.1f%%', wedgeprops={'edgecolor': 'black'})
        plt.title("Economic Status")
        plt.tight_layout()
        plt.show()

    def plot_education(self):
        plt.style.use("fivethirtyeight")
        labels = ["Some Elementary", "Elementary Graduate", "Some High School", "High School Graduate",
                                  "Some College", "Bachelor's Degree", "Vocational", "Advanced Degree"]
        explode = [0, 0, 0, 0, 0, 0.1, 0, 0]

        plt.pie(self.educ_tally, labels=labels, explode=explode, shadow=True, startangle=90, autopct='%1.1f%%',
                wedgeprops={'edgecolor': 'black'})
        plt.title("Education Status")
        plt.tight_layout()
        plt.show()
