<h1>VulnWiper</h1>

<p>An AI Cybersecurity Solution submitted for the TECS competition. The main project files can be found under /VulnWiper. /SampleWebsite is a test php website with intentional vulnerabilities that the AI is supposed to fix.</p>

<h3>Red AI</h3>
 
<p>The script used to launch an attack on a website can be found under /VulnWiper/RedTeam/MainAttack.py. Simply change the targetURL to the URL of the website you wish to perform a test on and run the script. The results of the attack will be found under /VulnWiper/Storage.json.</p>
 
<h3>Blue AI</h3>

<p>The script used to find and fix vulnerabilities can be found under /VulnWiper/BlueTeam/MainPatch.py. You can change the targetProject path to a different project, but you will need to configure routes, as can be seen under /SampleWebsite/routes.json, otherwise the script will not work. Note that the fixing AI is currently disabled, as such the only output is from the AI responsible for locating the vulnerability in the code.</p>

<h3>Sample Website</h3>

<p>There is a sample website built in php that can be run with the command "php -S localhost:8000 -t SampleWebsite/public". You can freely explore the website by visiting http://localhost:8000/ after running the command. Note that the AI will be unable to perform tests on the sample website until it is running.</p>
