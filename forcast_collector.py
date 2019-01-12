from bs4 import BeautifulSoup
import urllib
import json

URL = "https://weather.com/weather/hourbyhour/l/isXX0034:1:is"
HEADERS = ('time', 'description', 'temp', 'feels', 'precip', 'humidity', 'wind')


# this function receives a table row and a header, and outputs the content of the specific table line
def get_header_content(row, header):

    # parse the html with lxml and soup
    row_soup = BeautifulSoup(str(row), "lxml")

    # finds the value of the given header
    header_value = row_soup.body.find('td', attrs={'headers': header})

    # if statement that checks if the header is not precip, and if it is handles it accordingly
    if not header == "precip":
        # finds the value of the given header
        header_value = header_value.span

    return header_value.text


# this function receives a table row and a list of headers, and outputs a json formatted dictionary,
# which is build from the row lines
def json_dict_builder(row, headers):

    data = {}    # declare data dict
    value = {}   # declare value dict

    # loop through the given headers except the time header ( because it is the key for the data dict ),
    # and insert the value into the value dict, while the key is the header name
    for header in headers[1:]:
        value[header] = get_header_content(row, header)

    # insert the value dict as value for the data dict, the key is the time header.
    data[get_header_content(row, headers[0])] = value

    return data


# general function for the script use, connects all the functions.
def forecast_collector(url):

    page = urllib.request.urlopen(url)   # Get the html from the website using urllib
    soup = BeautifulSoup(page, "lxml")   # parse it with soup and lxml
    table = soup.body.find('table', attrs={'class': 'twc-table'})   # parse the site and get the wanted table
    rows = table.find_all('tr')  # parse the table to table rows

    # open file to write to
    with open('forcast_data.json', 'w') as outfile:

        # loop through the table rows from row 1 (row 0 is only headers, so it's not needed)
        for row in rows[1:]:

            # output the dict from json_dict_builder in a json format to outfile
            json.dump(json_dict_builder(row, HEADERS), outfile)


def main():

    # run the function on URL variable which is declared at the start of the script.
    forecast_collector(URL)


if __name__ == "__main__":

    main()
