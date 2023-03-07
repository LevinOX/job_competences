import requests
import base64

requests.packages.urllib3.disable_warnings()
ad_number = 5
searchText = "python, aws, erneuerbare energie*"
location = "Deutschland"
writemode = 'w'

# TODO: refactor/cleanup: outsource functions to functions2.py

def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def store_refnr(list_nrs):
    with open('known_refnrs.txt', writemode) as known:
        for nr in list_nrs:
            print(nr, file=known)

def clean_refnrs(refnrs):
    known_refnrs = read_file('known_refnrs.txt')
    clean_numbers = [
        nr for nr in refnrs if nr not in known_refnrs]
    return clean_numbers

def get_jwt():
    """fetch the jwt token object"""
    headers = {
        'User-Agent': 'Jobsuche/2.9.2 (de.arbeitsagentur.jobboerse; build:1077; iOS 15.1.0) Alamofire/5.4.4',
        'Host': 'rest.arbeitsagentur.de',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }

    data = {
      'client_id': 'c003a37f-024f-462a-b36d-b001be4cd24a',
      'client_secret': '32a39620-32b3-4307-9aa1-511e3d7f48a8',
      'grant_type': 'client_credentials'
    }

    response = requests.post('https://rest.arbeitsagentur.de/oauth/gettoken_cc', headers=headers, data=data, verify=False)
    #response = requests('POST', 'https://rest.arbeitsagentur.de/oauth/gettoken_cc', headers=headers, data=data, verify=False)

    return response.json()

def search(jwt, what, where):
    """search for jobs. params can be found here: https://jobsuche.api.bund.dev/"""
    params = (
        ('angebotsart', '1'),
        ('page', '1'),
        ('pav', 'false'),
        ('size', ad_number),
        ('umkreis', '25'),
        ('was', what),
        ('wo', where),
    )

    headers = {
        'User-Agent': 'Jobsuche/2.9.2 (de.arbeitsagentur.jobboerse; build:1077; iOS 15.1.0) Alamofire/5.4.4',
        'Host': 'rest.arbeitsagentur.de',
        'OAuthAccessToken': jwt,
        'Connection': 'keep-alive',
    }

    response = requests.get('https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/app/jobs',
                            headers=headers, params=params, verify=False)
    return response.json()


def get_job_details(jwt, job_ref):

    headers = {
        'User-Agent': 'Jobsuche/2.9.3 (de.arbeitsagentur.jobboerse; build:1078; iOS 15.1.0) Alamofire/5.4.4',
        'Host': 'rest.arbeitsagentur.de',
        'OAuthAccessToken': jwt,
        'Connection': 'keep-alive',
    }

    response = requests.get(
        f'https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v2/jobdetails/{(base64.b64encode(job_ref.encode())).decode("UTF-8")}',
        headers=headers, verify=False)

    return response.json()


if __name__ == "__main__":
    jwt = get_jwt()
    result = search(jwt["access_token"], searchText, location)

    #refnrs = result['stellenangebote'][:]["refnr"]
    refnrs = [job['refnr'] for job in result['stellenangebote']]
    refnrs = clean_refnrs(refnrs)
    print("len(refnrs): ", len(refnrs))


    # save the data in txt-file with the lines:
    #   URL             externeUrl
    #   job title       titel
    #   company:        arbeitgeber
    #   job description:stellenbeschreibung
    f = open("job_descriptions_arbeitsagentur_api.txt",
             writemode, encoding='utf-8')
    # print(result['stellenangebote'][0])

    for i in range(n := len(refnrs)):
        print("i is ", i)
        job_details = get_job_details(jwt["access_token"], refnrs[i])
        try:
            URL = job_details["externeUrl"]
        except:
            try:
                URL = job_details["arbeitgeberdarstellungUrl"]
            except:
                URL = job_details["allianzpartnerUrl"]
        job_title = job_details["titel"]
        profession = job_details["beruf"]
        company = job_details["arbeitgeber"]
        refnr = refnrs[i]
        date = job_details["aktuelleVeroeffentlichungsdatum"]
        place = job_details["arbeitgeberAdresse"]
        job_description = job_details["stellenbeschreibung"]
        f.writelines((URL + '\n',
                    refnr + '\n',
                    date + '\n'
                    f"{job_title}, {profession} \n",
                    company + '\n',
                    str(place) + '\n',
                    job_description.strip() + '\n\n'))
    f.close()
    store_refnr(refnrs)