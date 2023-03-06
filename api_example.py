import requests
import base64
import certifi
#import urllib3
requests.packages.urllib3.disable_warnings()
ad_number = 100

print("\n\n# # # # # script starts here # # # # #\n")
# http.request('GET', 'https://google.com')
# http.request('GET', 'https://expired.badssl.com')

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


def job_details(jwt, job_ref):

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
    print("I'm main.")
    jwt = get_jwt()
    result = search(jwt["access_token"], "bahn", "berlin")


    # save the data in txt-file with the lines:
    #   URL             externeUrl
    #   job title       titel
    #   company:        arbeitgeber
    #   job description:stellenbeschreibung
    f = open("job_descriptions_arbeitsagentur_api.txt",
             "w", encoding='utf-8')
    for i in range(ad_number):
        print("i is ", i)
        source = "none"
        try:
            source = "externeUrl"
            URL = job_details(jwt["access_token"], result['stellenangebote'][i]["refnr"])["externeUrl"]
        except:
            try:
                source = "arbeitgeberdarstellungUrl"
                URL = job_details(jwt["access_token"], result['stellenangebote'][i]["refnr"])["arbeitgeberdarstellungUrl"]
            except:
                source = "allianzpartnerUrl"
                URL = job_details(jwt["access_token"], result['stellenangebote'][i]["refnr"])["allianzpartnerUrl"]
        finally:
            print(f"URL given by {source}.")
        job_title = job_details(jwt["access_token"], result['stellenangebote'][i]["refnr"])["titel"]
        profession = job_details(jwt["access_token"], result['stellenangebote'][i]["refnr"])["beruf"]
        company = job_details(jwt["access_token"], result['stellenangebote'][i]["refnr"])["arbeitgeber"]
        job_description = job_details(jwt["access_token"], result['stellenangebote'][i]["refnr"])["stellenbeschreibung"]
        f.writelines((URL + '\n',
                    f"{job_title}, {profession} \n",
                    company + '\n',
                    job_description.strip() + '\n\n'))
    f.close()