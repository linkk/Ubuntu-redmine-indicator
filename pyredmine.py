# - coding: utf-8 -

#from mechanize import DefaultFactory, Browser
#from pyactiveresource.activeresource import ActiveResource
from lazr.restfulclient._browser import Browser
from pyactiveresource.activeresource import ActiveResource
import appindicator
import gobject
import gtk
import logging
import os
import xml.dom.minidom
import sys

HOST = 'http://redmine.bring.out.ba'
USER = 'jasox'
PASSWORD = '0000000000'

class PyRedmine:
    """Represents PyRedmine Object"""    

    def __init__(self, host=None, user=None, password=None):
        """Initialize object"""

        self.host = host
        self.user = user
        self.password = password

        # Initialize ActiveResource Objects
        self.projects = self.Project
        self.issues = self.Issue

        HOST = host
        USER = user
        PASSWORD = password

        #self.mech = Browser(DefaultFactory(i_want_broken_xhtml_support=True))


    class Project(ActiveResource):
        """Represents Projects object"""
        
        _site = HOST
        _user = USER
        _password = PASSWORD


    class Issue(ActiveResource):
        """Represents Issues object"""
    
        #HOST = 'http://www.redmine.org'
        
        _site = HOST
        _user = USER
        _password = PASSWORD

        Journals = []
        Changesets = []

        def journal_updates(self):

            all_data = []
            try:
                for journal in self.journals.journal:
                    all_data.append(journal.attributes)
            except:
                pass

            return all_data

        def changeset_updates(self):
            
            all_data = [] 
            try:
                for changeset in self.changesets.changeset:
                    all_data.append(changeset.attributes)
            except:
                pass

            return all_data


    def get_projects(self, options=None):
        """Get all projects"""
   
        return self.projects.find()

    def get_project(self, id):
        """Get an specific Project"""
   
        return self.projects.find(id)

    def get_issues(self, options=None):    
        """Get all issues with or without a search criteria

        attrs
          options: may be a dict of search criteria
        returns
          If issues were found, return an array of issues"""

        ## TODO: Re-code this, please!!
        ## Not better way to parse options
        if (options):
            opt_string = ''
            for criteria in options.keys():
                opt_string = opt_string + criteria + '=' + options[criteria] + '&'

            options = HOST + '/issues.xml?' + opt_string[:-1]
            return self.issues.find('', options)
        
        return self.issues.find()
        
    def get_issue(self, id):
        """Get an specific issue, given by id"""
        
        issue = self.issues.find(id)
        issue.Journals = issue.journal_updates()
        issue.Changesets = issue.changeset_updates()

        return issue

    ## ESTE METODO DESAPARECERA    
    def get_issue_details(self, id):
        """Get an extended info from an specific issue, given by id"""
       
        #self.journals.journal

        ### CORREGIR
         
        for journal in [x.attributes for x in self.journals.journal]:
            self.updates['journals'].append(journal)
    
        for changeset in [x.attributes for x in self.changesets.changeset]:
            self.updates['changesets'].append(changeset)
 
        return self.issues.updates
   
        ###

    def get_journals(self):
        print 'dummy function!'

        return self.issues.journals.journal

    def get_changesets(self, issue):
        print 'dummy function!'

    def create_issue(self, issue):
        
        new_issue = self.issues.create(issue)
        return new_issue
        

    def update_issue(self, changes):
        print 'dummy function!'

        self.save()
        return True
 

    def create_journal(self, issue):
        print 'dummy function!'

    def commit(self):
        print 'dummy function!'
    

## MECHANIZE SIDE ?!?!?
## Workflow:
##  
## br = Browser(DefaultFactory(i_want_broken_xhtml_support=True))
## br.open('file:///tmp/foo.html')
## br.select_form(nr=0) # or br.select_form(name='tracker_id')
## control = br.form.find_control(name='item') # to select specific combo
## for item in control.items:
##     print item.attrs    
##

    def get_project_trackers(self, project_id):
        print 'dummy function'

    def get_project_members(self, project_id):
        print 'dummy function'

    def get_project_status(self, project_id):
        print 'dummy function'

    def get_project_categories(self, project_id):
        print 'dummy function'
    
    def login(self):
        print 'dummy function'


def menuitem_response(w, buf):
    print buf

demo = PyRedmine(HOST, USER, PASSWORD)
issue24943 = demo.get_issue(24943)
print issue24943.Journals

if __name__ == "__main__":

    ind = appindicator.Indicator ("Redmine indicator", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
    ind.set_status (appindicator.STATUS_ACTIVE)
    ind.set_icon_theme_path("/home/jasmin/workspaceAptana/RedmineIndicator")
    ind.set_icon("redmineLogo")
    # create a menu
    menu = gtk.Menu()

    # create some 
    buff = [ "Connect", "Quit" ]

    menu_items = gtk.MenuItem(buff[0])
    menu.append(menu_items)
  
    menu_items = gtk.MenuItem(buff[1])
    menu.append(menu_items)

    # this is where you would connect your menu item up with a function:
    
    menu_items.connect("activate", menuitem_response, buff[1])
    
    # show the items
    menu.show_all()

    ind.set_menu(menu)
    
    
    gtk.main()
    






