# Web Scraping Script

This script will extract information from https://www.kayak.co.in/ and save into databases.<br>

#Teachnology Used in This Project:
1. Python <br>
2. Selenium Webdriver <br>
3. MySQL <br>
4. peewee <br>
5. cryptography <br>
6. pymysql <br>

#How to install this project:<br>
First create virtual environment and then clone the repository using following command. <br>
<code> git clone https://github.com/RashedEmon/scraping.git</code>  <br>
Change directory to project root folder <br>
<code>cd scraping</code><br>
Install all the depedency of the project<br>
<code>pip install -r requirements.txt</code><br>
Download and install mysql server and configure by using following values(you can customize the values. But You have to change the value in database module)<br>
username: mysql<br>password: mysql<br>database name: mysql<br>host: localhost<br>port: 3306<br>
Run the script by following command<br>
<code>python3 index.py</code>

#Database Schema<br>
Hotel(id,name)<br>
Images(id,hotel_id,image,label_id)<br>
Label(id,name)<br>


