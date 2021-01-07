import tkinter as tk
from tkinter import StringVar
from bs4 import BeautifulSoup
from googlesearch import search
import requests
import webbrowser

# Main window settings and title
root = tk.Tk()
root.title("RateMyProfessor Extension")
root.maxsize(650,500)
root.minsize(650,500)

google = False # If this is false, more_info function returns no results to get more info on. If get_information() function returns results, google sets to True

def get_information():

    global google
    name = professor_name_var.get()
    school = professor_institution_var.get()
    bottom_text_output.delete("1.0", tk.END)
    professor_search = f"{name} {school} RateMyProfessor"

    # gets url from professor's rate my professor page
    for s in search(professor_search, tld="co.in", num=1, stop=1, pause=1):
        url = s  # url, only does one search, stops at first option.

    # Checks to see if the professor is in rate my professor
    if 'ratemyprofessor' in str(url).split("/")[2]:
        try:
            # Draws html contents from the provided url
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Information indexing and cleaning
            prof_name = soup.find(class_="NameTitle__Name-dowf0z-0 cfjPUG").get_text()
            rating = soup.find(class_="RatingValue__Numerator-qw8sqy-2 liyUjw").get_text()
            number_of_ratins = soup.find(class_="RatingValue__NumRatings-qw8sqy-0 jMkisx").get_text().replace('Overall Quality ', '')
            would_take_again = soup.find(class_="FeedbackItem__FeedbackNumber-uof32n-1 kkESWs").get_text()
            stundet_review = str(soup.find('div', {"class": "TeacherRatingTabs__StyledTabs-pnmswv-0 lloXQq"}).find_all(class_="Comments__StyledComments-dzzyvm-0 gRjWel")).replace('</div>,', '').split('<div class="Comments__StyledComments-dzzyvm-0 gRjWel">')


            bottom_text_output.insert(tk.END, f"Name: {prof_name}\n")
            bottom_text_output.insert(tk.END, f"Institution: {school}\n")
            bottom_text_output.insert(tk.END, f"Rating: {rating}/5\n")
            bottom_text_output.insert(tk.END, f"{number_of_ratins}\n")
            bottom_text_output.insert(tk.END, f"Would take again: {would_take_again}\n\n")
            google = True

            for item in range(6):
                bottom_text_output.insert(tk.END, f"{item + 1}) {stundet_review[item + 1]}\n\n")
        except AttributeError:
            print("This professor is not available to check")
            bottom_text_output.insert(tk.END, "\n\n\n\n\n\n\n\nThis professor is not available to check\nNothing entered or check for misspellings")
    else:
        bottom_text_output.insert(tk.END, "\n\n\n\n\n\n\n\nThis professor is not available to check\nNothing entered or check for misspellings")

# Once info is returned, you can look up more info on the rate my professor page.
def get_more_information():
    if google == True:
        name = professor_name_var.get()
        school = professor_institution_var.get()

        professor_search = f"{name} {school} RateMyProfessor"
        for s in search(professor_search, tld="co.in", num=1, stop=1, pause=1):
            url = s  # url, only does one search, stops at first option.

        webbrowser.open(url)
    else:
        bottom_text_output.delete("1.0", tk.END)
        bottom_text_output.insert(tk.END, "\n\n\n\n\n\n\n\nNo Professor Information to Look Up")


# Strings to get inputs from entries
professor_name_var = StringVar()
professor_institution_var = StringVar()

# GUI Code
main_frame = tk.Frame(root, bg='grey')
main_frame.pack(fill='both', expand=True)

top_frame = tk.Frame(main_frame, bg='grey')
top_frame.place(relwidth=1, relheight=0.2)

professor_name_entry = tk.Entry(top_frame, textvariable=professor_name_var)
professor_name_entry.place(relx=0.3, rely=0.18)

institution_name_entry = tk.Entry(top_frame, textvariable=professor_institution_var)
institution_name_entry.place(relx=0.3, rely=0.58)

professor_name_entry_label = tk.Label(top_frame, text='Professor')
professor_name_entry_label.place(relx=0.14, rely=0.18)

professor_name_entry_label = tk.Label(top_frame, text='Institution')
professor_name_entry_label.place(relx=0.14, rely=0.58)

submit_button = tk.Button(top_frame, text='Get Information', command=lambda: get_information())
submit_button.place(relx=0.7, rely=0.17)

more_info = tk.Button(top_frame, text='More Info', command=lambda: get_more_information())
more_info.place(relx=0.7, rely=0.6)

bottom_text_output = tk.Text(main_frame, bg='light grey')
bottom_text_output.place(relwidth=0.9, relheight=0.7, relx=0.05, rely=0.25)

root.mainloop() # Allows window to run until closed
