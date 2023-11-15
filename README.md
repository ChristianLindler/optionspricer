## Options Pricing Overview
A full stack application that utilizes the Heston Model and Longstaff Schwartz approach to price American and European Options

Access the site at https://www.optionspricerapp.com/

![App Screenshot](images/app_pic.png)

## Usage
The user interface is very intuitive. In the top left of the application there is a form where users first enter a stock ticker they would like to price an option on. YFinance is used to collect stock data, so only options can only be priced on stocks who's data is available through YFinance.
Other parameters (Strike price, time-to-expiry, number of simulations) are selected in the same form. When the parameters are selected, the "Calculate" button is used to begin calculating Options Price.
Upon calculation, the application visualizes 100 of the user's simulated paths, the standard error for American Prices, and a distrubution of the returns on the final day.

## Built With
* <a href="https://reactjs.org/"><img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" width="100"></a>
* <a href="https://flask.palletsprojects.com/en/3.0.x/"><img src="https://flask.palletsprojects.com/en/3.0.x/_images/flask-horizontal.png" alt="Flask" width="100"></a>

## Credits
<ul>
   <li>
      <b>Christian Lindler</b>
      <a href="www.linkedin.com/in/christianlindler"><img src="https://cdn1.iconfinder.com/data/icons/logotypes/32/circle-linkedin-512.png" alt="Linkedin" width="30"></a>
      <a href="https://github.com/ChristianLindler"><img src="https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png" alt="GitHub" width="30"></a>
      <a href="mailto:ChristianWLindler@gmail.com"><img src="https://static.vecteezy.com/system/resources/previews/016/716/465/non_2x/gmail-icon-free-png.png" alt="Email" width="30"></a>
   </li>
   <li>
      <b>
         Ben DiPrete
      </b>
   </li>
   <li>
      <b>
         Cole Miller
      </b>
   </li>
</ul>
