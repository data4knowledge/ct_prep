from datetime import datetime
from drive.drive import Drive

class Manifest():

  def __init__(self):
    self.__drive = Drive("manifest")
    self.__manifest = self.__drive.read('manifest.yaml')
  
  def next_release_after(self, this_date):
    dates = {}
    for date_str in self.__manifest.keys():
      manifest_date = self._from_iso8601_str(date_str)
      diff = manifest_date - this_date
      if diff.days > 0:
        dates[diff.days] = date_str
    return dates[min(dates.keys())]

  def release_list(self, start_date):
    releases = []
    start_date_as_date = self._from_iso8601_str(start_date)
    for date_str in self.__manifest.keys():
      manifest_date = self._from_iso8601_str(date_str)
      diff = manifest_date - start_date_as_date
      if diff.days >= 0:
        print(self.__manifest[date_str])
        releases.append({'date': date_str, 'owner': self.__manifest[date_str]['owner']})
    return releases

  def concept_scheme_list(self, release_date):
    #print("CONCEPT_SCHEME_LIST [1]:", release_date)
    #print("CONCEPT_SCHEME_LIST [2]:", self.__manifest[release_date])
    results = []
    for k, v in self.__manifest[release_date]["items"].items():

      # FOR TEST!!!
#      if k != "adam":
#        continue

      date, format_for_date = self._format_and_date(release_date, k)
      results.append({ 'scheme': k, 'release_date': release_date, 'date': date, 'format': format_for_date })  
    #print("CONCEPT_SCHEME_LIST [3]:", results)
    return results

  def _from_iso8601_str(self, text):
    return datetime.strptime(text, '%Y-%m-%d').date()

  def _to_iso8601_str(self, date):
    return date.strftime("%Y-%m-%d")

  def _format_and_date(self, release_date, scheme):
    date = self.__manifest[release_date]["items"][scheme]
    format = self._api_or_file(date)
    return date, format

  def _api_or_file(self, date):
    if "api" in self.__manifest[date]["format"]:
      return "api"
    else:
      return "file"
