"""
Python oxford date module.
"""

# Note on the extended strftime syntax:
#  %u - Oxford term week number
#  %t - Oxford term, short name
#  %T - Oxford term, long name


import math
import datetime
import time

def d(y,m,d): return datetime.datetime(int(y),int(m),int(d))

def rdict(d):
    return dict([(y,x) for x,y in d.items()])



terms = {
    d(1970,1,1): ("Null", 0),
    d(1999,1,7): ("hilary", 1999),
    d(1999,4,20): ("trinity", 1999),
    d(1999,10,10): ("michaelmas", 1999),
    d(2000,1,16): ("hilary", 2000),
    d(2000,4,30): ("trinity", 2000),
    d(2000,10,8): ("michaelmas", 2000),
    d(2001,1,14): ("hilary", 2001),
    d(2001,4,22): ("trinity", 2001),
    d(2001,10,7): ("michaelmas", 2001),
    d(2002,1,13): ("hilary", 2002),
    d(2002,4,21): ("trinity", 2002),
    d(2002,10,13): ("michaelmas", 2002),
    d(2003,1,19): ("hilary", 2003),
    d(2003,4,27): ("trinity", 2003),
    d(2003,10,12): ("michaelmas", 2003),
    d(2004,1,18): ("hilary", 2004),
    d(2004,4,25): ("trinity", 2004),
    d(2004,10,10): ("michaelmas", 2004),
    d(2005,1,16): ("hilary", 2005),
    d(2005,4,24): ("trinity", 2005),
    d(2005,10,9): ("michaelmas", 2005),
    d(2006,1,15): ("hilary", 2006),
    d(2006,4,23): ("trinity", 2006),
    d(2006,10,8): ("michaelmas", 2006),
    d(2007,1,14): ("hilary", 2007),
    d(2007,4,22): ("trinity", 2007),
    d(2007,10,7): ("michaelmas", 2007),
    d(2008,1,13): ("hilary", 2008),
    d(2008,4,20): ("trinity", 2008),
    d(2008,10,12): ("michaelmas", 2008),
    d(2009,1,18): ("hilary", 2009),
    d(2009,4,26): ("trinity", 2009),
    d(2009,10,11): ("michaelmas", 2009),
}

abbrs = {
    "hilary": "HT",
    "michaelmas": "MT",
    "trinity": "TT",
}

term_starts = rdict(terms)

r_abbrs = rdict(abbrs)


class NoIdeaError(StandardError):
    pass


class OxfordDate(object):
    
    def __init__(self, year, month=None, day=None):
        if month is None:
            if isinstance(year, OxfordDate):
                self.datetime = year.datetime
            else:
                self.datetime = year
        else:
            if isinstance(month, str):
                try:
                    mdt = time.strptime(month, "%B")
                    month = mdt[1]
                except ValueError:
                    mdt = time.strptime(month, "%b")
                    month = mdt[1]
            self.datetime = d(year, month, day)
        self.calc()
    
    @classmethod
    def from_oxford(cls, year, term, week=1, day="sunday"):
        #todo: optimise this
        if term.upper() in r_abbrs:
            term = r_abbrs[term.upper()]
        oxweek = OxfordWeek(year, term, week)
        dayno = (time.strptime(day, "%A")[6] + 1) % 7
        return cls(list(oxweek.days())[dayno])
    
    
    def calc(self):
        self.weekday = self.datetime.strftime("%A")
        self.shortweekday = self.datetime.strftime("%a")
        self.veryshortweekday = self.shortweekday[0]
        self.termstart = self.get_start()
        try:
            self.term, self.year = terms[self.termstart]
        except KeyError:
            raise NoIdeaError
        self.week = self.nth_week(self.termstart)
        self.shortname = "%s, Week %s, %s" % (self.weekday, self.week, self.term.title())
        self.name = "%s, Week %s, %s %s" % (self.weekday, self.week, self.term.title(), self.year)
        self.datestr = self.datetime.strftime("%Y/%m/%d")
    
    
    def strftime(self, format):
        format = format.replace("%u", str(self.week)).replace("%t", abbrs[self.term]).replace("%T", self.term.title())
        return self.datetime.strftime(format)
    
    
    def get_start(self):
        starts = terms.keys()
        starts.sort()
        for start in starts:
            if self.datetime < start:
                prev = starts[starts.index(start)-1] + datetime.timedelta(56,0)
                if (self.datetime < prev) or ((self.datetime - prev) < (start - self.datetime)):
                    return prev - datetime.timedelta(56,0)
                else:
                    return start
    
    
    def __repr__(self):
        return "<%s>" % self.shortname
    
    
    def nth_week(self, start):
        delta = self.datetime - start
        n = int(delta.days / 7) + 1
        return n
    
    
    def get_week(self):
        return OxfordWeek(self.year, self.term, self.week)
    
    
    @classmethod
    def weeks(self, year, term):
        for i in range(8):
            yield OxfordWeek(year, term, i+1)


class OxfordWeek(object):
    
    def __init__(self, year, term="hilary", n=1):
        self.year = int(year)
        self.term = term.lower()
        self.termyear = "%s%02i" % (abbrs[self.term], int(self.year) % 100)
        self.n = n
        try:
            self.term_start = term_starts[(self.term, self.year)]
        except:
            raise NoIdeaError("Date %s, %s out of knowledge range." % (self.term, year))
        self.start = self.term_start + datetime.timedelta(7*(n-1))
    
    
    def days(self):
        for i in range(7):
            yield OxfordDate(self.start + datetime.timedelta(i))
    
    
    def __str__(self):
        return "Week %s, %s %s" % (self.n, self.term.title(), self.year)
    
    
    def __repr__(self):
        return "<%s>" % self.__str__()

def oxweek2oxdate(year=None, term=None, week=None):
    """
    Takes a year, or a year and a term, or a year, week and a term as strings
    or strings and ints. Returns an OxfordDate object
    """
    try:
        year = int(year)
    except:
        raise NoIdeaError("Year '%s' doesn't convert to an int." % year)
    if term:
        # TODO: Allow for abbreviations of terms as well.
        try:
            term_start = term_starts[(term, year)]
        except:
            raise NoIdeaError("Date %s, %s out of knowledge range." % (term, year))
        if week:
            try:
                int(week)
            except:
                raise NoIdeaError("Year '%s' doesn't convert to an int." % year)
            return OxfordDate(term_start + datetime.timedelta(week=(week-1)))
        return OxfordDate(term_start)
    return OxfordDate(datetime.datetime(year, 1, 1))


