# -*- coding: utf-8 -*-

import email.message, email.parser, email, json, re, email.utils, urllib2, time, math
from os import listdir
from time import strftime
from datetime import datetime


new_name_dict = {'Sanchez, Daniel':'Rep. Gloria Negrete McLeod','Sen. Jay Rockefeller (Rockefeller)':'Sen. John Rockefeller IV','Aumua Amata':'Congresswoman Amata Radewagen','Congresswoman Aumua Amata':'Congresswoman Amata Radewagen','Congresswoman Loretta Sanchez':'Congresswoman Loretta Sánchez', 'Toni Porter':'Congressman Mike Pompeo','Congressman Tony Cardenas':'Congressman Tony Cárdenas', 'Senator Robert Menendez':'Senator Robert Menéndez', 'U.S. Senator Bob Menendez':'Senator Robert Menéndez','U.S. Senator Robert Menendez':'Senator Robert Menéndez','Fred':'Fred Upton', 'ROGERS E-NEWS':'Congressman Hal Rogers','kilili, e':'Gregorio Kilili Camacho Sablan','Eric Steklow': 'Ami Bera', 'Afnan Rashid': 'Hansen Clarke', 'Sharon Wallca': 'Hansen Clarke', 'Laurel Makries': 'Hansen Clarke', 'Rory Sheehan': 'Bill Delahunt', 'TX29Newsletters': 'Gene Green', 'Veronica Custer': 'Gene Green', 'Ashley Nagoaka': 'Colleen Hanabusa', 'Nathan White': 'Congressman Dennis Kucinich', 'CA33TLIMA': 'Ted Lieu', 'Daniel Schwarz':'Jerry Nadler','Maura Cordova':'Ed Pastor','Campbell, Nyaesia':'Terri Sewell', 'Jefferson, Deshundra':'Terri Sewell','NJ10DPima@mail.house.gov':'Donald Payne','MN07, Subscriptions':'Collin Peterson','Jose Borjon':'Silvestre Reyes', 'Claudia L. Ordaz':'Silvestre Reyes','Newsletter, MD02':'Dutch Ruppersberger','Richmond, Tavita':'Eni Faleomavaega','Rebecca.Alery@mail.house.gov':'Tom Emmer', 'Parker, Eric':'Frederica Wilson', 'Dan.Kotman@mail.house.gov':'Michele Bachmann', "The Leader's Daily Schedule":'Eric Cantor','Wasserstein, Rebecca':'Carlos Curbelo','Newsletter, MO08':'Jo Ann Emerson', 'Sok, Justin':'Jo Ann Emerson','Meghan Snyder':'Jim Jordan','Landon, Justin':'Jerry Lewis','Blue Angels':'Buck McKeon','CapitolConnection Newsletter':'Gary Miller','RonRaulmedia':'Ron Paul','sessions.newsletter@mail.house.gov':'Pete Sessions','Times, Thompson':'Glenn Thompson','David':'David Valadao','Mail___Outbound/Computerworks/US%MI09@US.House.gov':'Sander Levin','newsletter@begich.senate.gov':'Senator Begich','noreply@begich.senate.gov':'Senator Begich','Buchsbaum, Andy (Cardin)':'Ben Cardin', 'senator':'Senator Conrad','Bryan DeAngelis':'Chris Dodd', 'correspondence_reply@lieberman.senate.gov':'Joe Lieberman','enewsletters@manchin.senate.gov':'Senator Manchin','senator@mikulski.senate.gov':'Senator Mikulski','Teare, Caitlin (Ben Nelson)':'Ben Nelson','Sarah Kaopuiki':'Senator Brian Schatz','George Carvalho - Office of Senator Whitehouse':'Senator Sheldon Whitehouse','Tony Simon':'Senator Sheldon Whitehouse','newsletter@bunning.senate.gov':'Senator Bunning','newsletter@ensign.senate.gov':'Senator Ensign','enewsletter@lgraham.senate.gov':'Senator Lindsey Graham','enewsletter@hoeven.senate.gov':'Senator John Hoeven','Office_SenJohanns@johanns.senate.gov':'Senator Mike Johanns','Mike_Johanns@johanns.senate.gov':'Senator Mike Johanns','JamesRisch_OutboxOnly@risch.senate.gov':'Senator James Risch','newsletter@shelby.senate.gov':'Senator Richard Shelby','Van der Lugt, Roel':'Adam Smith','Kildee eNewsletter':'Dale Kildee', 'Senator Bob Menendez':'Senator Robert Menéndez','MN01Newsletter':'Congressman Tim Walz','Langer, Jack':'Devin Nunes','Fred ':'Fred Upton','Andre':'Andre Carson','Brad':'Brad Wenstrup','The Civil Rights Act of 1964':'Congressman Bill Foster',"Donna's Newsletter":'Donna Christensen','Villari, Gena':'Eric Cantor','Cordova, Maura':'Ed Pastor','Langer, Jack':'Devin Nunes','Phelan, Richard Andrew':'Hank Johnson','Wes Battle': 'Congressman J. Randy Forbes','Maggie Seidel':'Congressman Morgan Griffith','Jennifer Hazelton':'Congressman Tom Graves','Nagaoka, Ashley':'Colleen Hanabusa','Winters, Natalie':'Congressman Collin C. Peterson','Mena, Sharlett':'Congressman Albio Sires','ROGERS NEWS':'Congressman Hal Rogers','Congressman Mario Diaz Balart':'Congressman Mario Diaz-Balart','Keystone Pipeline':'Congressman Blaine Luetkemeyer','IN08enews':'Congressman Larry Bucshon','Entenman, Debra':'Congressman Adam Smith','Beth Breeding':'Congressman Morgan Griffith','Fennick, Renita':'Tom Marino','e-news-wi06':'Congressman Tom Petri','MSNBC Interview Tonight on Inequality in America':'Congressman John Garamendi', 'Cary Wright':'Congressman Mac Thornberry','Manufacturing Caucus':'Congressman Don Manzullo', 'Vincent M. Perez':'Representative Silvestre Reyes','Kingston Press Office':'Congressman Jack Kingston','Ashley L. Muschnick':'Congressman Ted Deutch','Breeding, Beth':'Morgan Griffith','MS04 Newsletter':'Congressman Steven Palazzo','Allison, William':'Congressman James Lankford','Rashid, Afnan':'Hansen Clarke','FL02ENEWS':'Congressman Steve Southerland','Ashley Mushnick':'Congressman Ted Deutch','NH02enews':'Congressman Charles Bass','Zimmerman, Stefani':'Congressman Paul Gosar','NewsletterNV03':'Congressman Joe Heck','Baron, Luke':'Congressman Adam Smith','Media, KS01':'Congressman Tim Huelskamp','CHUCK GRASSLEY':'Senator Chuck Grassely','Drogus, Jennifer':'Congressman Rob Woodall','KINGSTONPRESSOFFICE@mail.house.gov':'Congressman Jack Kingston','Popelka, Brecke':'Representative Martha Roby','Abney, Allison':'Congresswoman Terri A. Sewell','e-Newsletter, VA05':'Congressman Robert Hurt','Rawat, Vinod':'Congresswoman Terri A. Sewell',"Norm's Newsletter":'Norm Dicks','Max News':'Senator Max Baucus','Sheehan, Rory':'Bill Delahunt','Shedd, Leslie':'Congressman Frank Lucas','Audra McGeorge':'Rep. Ed Royce','Sillin, Nathaniel':'Congressman Mike Coffman','Andel, Michael':'Congressman David Scott','Orme, Katie':'Congressman John Shadegg','Slusher, Eric':'Congresswoman Niki Tsongas','Brock McCleary':'Congressman Patrick McHenry', 'Congressman Ben Ray Lujan':'Congressman Ben Luján', 'Congresswoman Linda Snchez':'Congresswoman Linda Sánchez', 'Congresswoman Linda T. Snchez':'Congresswoman Linda Sánchez','Congresswoman Linda Sanchez':'Congresswoman Linda Sánchez', 'Sarah Kuziomko':'Congressman Tim Walberg', 'Assistant Democratic Leader Press':'Congressman James E. Clyburn','Newsletter, IN07':'Congressman André Carson', 'Congressman Ben Ray Lujn':'Congressman Ben Ray Luján', 'KINGSTON PRESS OFFICE':'Congressman Jack Kingston', 'Ashley L. Mushnick':'Congressman Ted Deutch','sessions.newsletter@mail.house.gov':'Congressman Jeff Sessions', 'CA33TLIMA@mail.house.gov':'Congressman Ted Lieu', 'Mail___Outbound/Computerworks/US%MO08@US.House.gov':'Congressman Jason Smith', 'newsletter_kirk@kirk.senate.gov':'Senator Mark Kirk','congressmanmikehonda-ca17@mail.house.gov':'Congressman Mike Honda','donotreplymikehondaupdates@mail.house.gov':'Congressman Mike Honda','senator@isakson.senate.gov':'Senator Johnny Isakson','Press_Office@carper.senate.gov':'Senator Tom Carper','senator_wyden@wyden.senate.gov':'Senator Ron Wyden','oh16Newsletter@mail.house.gov':'Congressman Jim Renacci','MN08RNIMA@mail.house.gov':'Congressman Rick Nolan','imanj10@mail.house.gov':'Congressman Donald M. Payne Jr.','KY06ABIMA@mail.house.gov':'Representative Andy Barr','ny20ima-113@mail.house.gov':'Congressman Paul Tonko','davidvitter@vitter.senate.gov':'Senator David Vitter','david_vitter@vitter.senate.gov':'Senator David Vitter','senator@conrad.senate.gov':'Senator Kent Conrad','matt.perry@mail.house.gov':'Congressman Adam Smith','roel.vanderlugt@mail.house.gov':'Congressman Adam Smith','debra.entenman@mail.house.gov':'Congressman Adam Smith','linh.thai@mail.house.gov':'Congressman Adam Smith','eNews@isakson.senate.gov':'Senator Johnny Isakson','shelley.berkley@mail.house.gov':'Congresswoman Shelley Berkley','enzi_newsletter@enzi.senate.gov':'Senator Mike Enzi','senator@mccaskill.senate.gov':'Senator Claire McCaskill','senator_levin@levin.senate.gov':'Senator Carl Levin','robert.goodlatte@mail.house.gov':'Congressman Bob Goodlatte','il03@housemail.house.gov':'Congressman Dan Lipinski','lamar_alexander@alexander.senate.gov':'Senator Lamar Alexander','David_vitter@vitter.senate.gov':'Senator David Vitter','newsletter@roberts.senate.gov':'Senator Pat Roberts','newsletter@inhofe.senate.gov':'Senator Jim Inhofe','do_not_reply@markudall.senate.gov':'U.S. Senator Mark Udall', 'Democratic Leader':'Representative Nancy Pelosi', 'Erin Moffet Hale':'Representative Patrick Murphy','Custer, Veronica':'Representative Gene Green','Matt Lira':'Representative Eric Cantor','Ben Veghte':'Representative Scott Garrett','Wallace, Sharon':'Represenative Hansen Clarke','George Carvalho':'Senator Sheldon Whitehouse', 'Congressman Luis Gutirrez': 'Luis Gutiérrez', 'Senator Bob Menendez': 'Robert Menéndez', 'senator@tomudall.senate.gov': 'Tom Udall', 'senator@tester.senate.gov': 'Jon Tester', 'Congresswoman Linda T. Snchez': 'Linda Sánchez', 'Grant Information': 'Orrin Hatch', 'Paucar, Theresa': 'Luis Gutiérrez', 'Senator@tomudall.senate.gov': 'Tom Udall', 'Congressman Tony Cardenas': 'Tony Cárdenas', 'U.S. Senator Robert Menendez': 'Robert Menéndez', 'Congressman Tony Crdenas': 'Tony Cárdenas', 'Eric Stecklow': 'Ami Bera', 'Congressman Ben Ray Lujan': 'Ben Luján', 'U.S. Senator Bob Menendez': 'Robert Menéndez', 'ted@tedcruz.org': 'Ted Cruz', 'Congresswoman Linda Snchez': 'Linda Sánchez', 'Senator Robert Menendez': 'Robert Menéndez', 'Dem Leader Press Office': 'Nancy Pelosi', 'Ortiz, Alvaro': 'Al Green', 'Newsletter, IN07': 'André Carson', 'Congressman Ben Ray Lujn': 'Ben Luján'}
bad_names = []

class Email(object):
    def __init__(self, email_path):
        '''Initializes an instance of the Email class.'''
        self.path = email_path
          
    def get_body(self):
        '''Stores the body of the email as an attribute, removing any whitespace characters and escapes.'''
        fp = open(self.path)   
        msg = email.message_from_file(fp)
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    self.body = remove_junk(str(part.get_payload(decode=True)))
                    if len(self.body) <= 16:
                        self.valid = False
                    return
        else:
            self.body = remove_junk(str(msg.get_payload(decode=True)))
            if len(self.body) <= 16:
                self.valid = False
            return
        
    def get_header(self):
        '''Gets header information from the email and stores it as attributes.'''
        fp = open(self.path)
        msg = email.message_from_file(fp)
        for item in msg.items():
            if item[0] == 'From':
                parsed_address = email.utils.parseaddr(item[1])
                self.name, encoding = email.Header.decode_header(parsed_address[0])[0]
                self.name = remove_non_ascii(self.name)
                self.address = parsed_address[1]
                if "google.com" in self.address or "Google.com" in self.address or "pols.exp@gmail.com" in self.address:
                    self.valid = False
                    return
                else:
                    self.valid = True
                if self.name == '':
                    self.name = self.address
                for entry in new_name_dict:
                    if self.name == entry:
                        self.name = new_name_dict[entry]
            if item[0] == 'Date':
                try:
                    self.date = strftime('%m/%d/%Y',email.utils.parsedate(item[1]))
                    self.month = strftime('%m',email.utils.parsedate(item[1]))
                    self.year = strftime('%Y',email.utils.parsedate(item[1]))
                except:
                    self.valid = False
            if item[0] == 'Subject':
                if item[1].startswith("=?utf-8?") or item[1].startswith("=?UTF-8?"):
                    self.subject, encoding2 = email.Header.decode_header(item[1])[0]
                    self.subject = remove_non_ascii(self.subject)
                    # ^^^ breaks program when encounters subject encoded with "iso-8859"
                else:
                    self.subject = item[1]
                    self.subject = remove_non_ascii(self.subject)

    def get_info(self):
        for member in self.congress:
            if member['last_name'] in self.name:
				if member['first_name'] in self.name:
					return pull_api_info(member)
				# search for first 2 letters of first name
				elif member['first_name'][:2] in self.name:
					return pull_api_info(member)
			#if there is a 3 letter name mod at the end of the last name
            elif member['last_name'][-3:] in ['Jr.', 'Sr.', 'III']:
				#cut off the last three characters
				if member['last_name'][:-4] in self.name:
					if member['first_name'] in self.name:
						return pull_api_info(member)
					# search for first 2 letters of first name
					elif member['first_name'][:2] in self.name:
						return pull_api_info(member)
			#if II is at the end of the last name
            elif member['last_name'][-2:] == 'II':
				#cut off the last two characters
				if member['last_name'][:-3] in self.name:
					if member['first_name'] in self.name:
						return pull_api_info(member)
				# search for first 2 letters of first name
				elif member['first_name'][:2] in self.name:
					return pull_api_info(member)
        return None

    def get_info_last_name_only(self):
        for member in self.congress:
            #If nothing matches, just go by last name
            if member['last_name'] in self.name:
                return pull_api_info(member)
            elif member['last_name'][-3:] in ['Jr.', 'Sr.', 'III']:
                #cut off the last three characters
                if member['last_name'][:-4] in self.name:
                    return pull_api_info(member)
            elif member['last_name'][-2:] == 'II':
                #cut off the last two characters
                if member['last_name'][:-3] in self.name:
                    return pull_api_info(member)
        if self.name not in bad_names:
            bad_names.append(self.name)
        
    def construct_dict(self):
        '''Constructs a dictionary of email information.'''
        self.get_header()
        self.get_body()
        if self.valid == False:
            return False
        try:
            email_dict = self.get_info()
            if email_dict == None:
                email_dict = self.get_info_last_name_only()
            email_dict['Subject'] = self.subject
            email_dict['Name'] = self.name
            email_dict['Address'] = self.address
            email_dict['Date'] = self.date
            email_dict['Body'] = self.body
            email_dict['Month'] = self.month
            email_dict['Year'] = self.year
            return email_dict
        except:
            return None
        
class Directory(Email):
    def __init__(self,directory):
        '''Initializes an instance of the Directory class.'''
        self.directory = directory
        self.congress = api_call()
        self.classifier = None
        
    def dir_list(self):
        '''Returns the list of all files in self.directory'''
        return listdir(self.directory)
        
    def dir_dict(self):
        '''Constructs a list of email dictionaries
        from a directory of .eml files.'''
        eml_list = []
        for email in self.dir_list():
            self.path = self.directory + '/' + email
            eml_dict = self.construct_dict()
            if eml_dict:
            	# Set full party name
            	if eml_dict['party'] == 'R':
            		eml_dict['party'] = 'Republican'
            	if eml_dict['party'] == 'D':
            		eml_dict['party'] = 'Democrat'
                eml_list.append(eml_dict)
        return eml_list
        
    def convert_json(self, json_path):
        '''Creates a json file of email information at the specified path.'''
        with open(json_path,'w') as json_file:
            json.dump(self.dir_dict(), json_file)
        
def remove_junk(string):
    '''Removes whitespace characters, escapes, and links from a string.'''
    string = re.sub(r'\s+', ' ', string)
    string = re.sub(r"[\x80-\xff]", '', string)
    link_regex=["<http.*?>","http.*? ","http.*?[^\s]\.gov","http.*?[^\s]\.com","http.*?[^\s]\.COM",
                "www.*?[^\s]\.com","www.*?[^\s]\.org","www.*?[^\s]\.net","www.*?[^\s]\.gov","/.*?[^\s]\.com",
                "/.*?[^\s]\.COM","/.*?[^\s]\.gov",",.*?[^\s]\.gov",",.*?[^\s]\.com",
                "<.*?>"]
    for curr in link_regex:
        string = re.sub(curr,'',string)
    return string

def remove_non_ascii(text):
    '''Removes any non-ascii characters from a string.'''
    return ''.join(i for i in text if ord(i)<128)

def get_current_congress():
    '''Returns the current Congress number'''
    base = datetime(2017, 1, 3) # January 3rd, 2017. When 115th Congress began
    now = datetime.now() # The current date

    leap_days = 0
    if now.year > 2020: # 2020 is the next leap year, so add 1 day for every 4 years after that
        leap_days = ((now.year - 2020) / 4) + 1 # this assumes DCInbox will be gone before the year 2100
                                                
    difference = now - base # datetime.timedelta difference between the 2 dates

    add_to_congress = int(math.floor( (float(difference.days - leap_days) / 365) / 2)) # get the number of congresses that have passed since 115
    return 115 + add_to_congress

def get_key():
    '''Returns the API key used for ProPublica'''
    with open('api_key.txt', 'r') as f:
        return f.read()

def api_call():
    '''Makes an api call and returns a list of information on the Congress members from the 111th-115th congress.'''
    members = []
    current_congress = get_current_congress()
    key = get_key()
    # Get House members for every relevant Congress
    for i in range(111, current_congress + 1):
        url = "https://api.propublica.org/congress/v1/" + str(i) + "/house/members.json"
        req = urllib2.Request(url)
        req.add_header('X-API-Key', key)
        res = urllib2.urlopen(req)
        content = json.loads(res.read())
        members += content['results'][0]['members']
        time.sleep(2)
    # Get Senate members for every relevant Congress
    for i in range(111, current_congress + 1):
        url = "https://api.propublica.org/congress/v1/" + str(i) + "/senate/members.json"
        req = urllib2.Request(url)
        req.add_header('X-API-Key', key)
        res = urllib2.urlopen(req)
        content = json.loads(res.read())
        members += content['results'][0]['members']
        time.sleep(2)
    return members

def pull_api_info(entry):
        '''Returns a dictionary of all the info from the API call.'''
        info_dict = {}
        bad_keys = ['youtube_account', 'rss_url', 'times_tag', 'times_topics_url', 'most_recent_vote', 'url', 'missed_votes_pct', 'phone', 'contact_form', 'bills_cosponsored']
        for key in entry.keys():
            if key not in bad_keys:
                info_dict[key] = entry[key]
        return info_dict

def main():
    '''Guides the user through the program.'''
    directory = '../2000_eml_files' #raw_input('Please enter the path to the directory of .eml files: ')
    json_fp = '../bulk_test.json' #raw_input('Please enter the location of the json file you would like to create: ')
    d = Directory(directory)
    d.convert_json(json_fp)
    print(bad_names)

 
if __name__ == '__main__':
    main()
