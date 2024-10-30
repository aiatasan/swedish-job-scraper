from scrapy.dupefilters import RFPDupeFilter
import sqlite3


class DatabaseDupeFilter(RFPDupeFilter):
    def __init__(self, path=None, debug=False, *, fingerprinter=None):
        super().__init__(path=path, debug=debug, fingerprinter=fingerprinter)
        self.conn = sqlite3.connect(path or "scrapy_dupefilter.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS visited_urls (url TEXT PRIMARY KEY)")
        self.conn.commit()

    # @classmethod
    # def from_settings(cls, settings, fingerprinter=None):
    #     path = settings.get('DUPEFILTER_CLASS')
    #     debug = settings.getbool('DUPEFILTER_DEBUG', False)
    #     return cls(path=path, debug=debug, fingerprinter=fingerprinter)


    def request_seen(self, request):
        url = request.url.lower()
        self.cursor.execute("SELECT 1 FROM visited_urls WHERE url = ?", (url,))
        if self.cursor.fetchone():
            return True

        self.cursor.execute("INSERT INTO visited_urls (url) VALUES (?)", (url,))
        self.conn.commit()
        return False

    def close(self, reason):

        self.conn.close()
