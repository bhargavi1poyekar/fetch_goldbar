# Bhargavi Poyekar: Fetch Challenge: GoldBar Weighing

## Table of Contents
- [Game Problem Statement](#game-problem-statement)
- [Flow Diagram](#flow-diagram)
- [Pseudocode](#pseudocode)
- [Run the code](#how-to-run-the-code)
- [Run without Docker](#run-without-using-docker)
- [File Structure](#file-structure)
- [Code Overview](#code-overview)
- [Challenges](#challenges)

## Game Problem Statement:

Given a balance scale and 9 gold bars of the same size and look. You don’t know the exact weight of each bar,
but you know they all weigh the same, except for one fake bar. It weighs less than others. You need to find the fake
gold bar by only bars and balance scales.
You can only place gold bars on scale plates (bowls) and find which scale weighs more or less.

## Flow Diagram:

![](https://i.postimg.cc/VNJ9gk3T/flowa-diagram-drawio.png)


## Pseudocode:

1. Initialize three groups of gold bars:
   Group A = {Bar1, Bar2, Bar3}
   Group B = {Bar4, Bar5, Bar6}
   Group C = {Bar7, Bar8, Bar9}

2. Weigh Group A against Group B:
   - If weight(Group A) == weight(Group B):
     - The fake bar is in Group C. Proceed to Step 3 using Group C.
   - If weight(Group A) < weight(Group B):
     - The fake bar is in Group A. Proceed to Step 3 using Group A.
   - If weight(Group A) > weight(Group B):
     - The fake bar is in Group B. Proceed to Step 3 using Group B.

3. Take the suspected group from Step 2 which contains three bars. Name them as Bar X, Bar Y, and Bar Z.

4. Weigh Bar X against Bar Y:
   - If weight(Bar X) == weight(Bar Y):
     - Bar Z is the fake bar.
   - If weight(Bar X) < weight(Bar Y):
     - Bar X is the fake bar.
   - If weight(Bar X) > weight(Bar Y):
     - Bar Y is the fake bar.

5. End algorithm.

## How to Run the code:

I assume that you have docker installed in your system. 

1. Clone Git repository:

        git clone "https://github.com/bhargavi1poyekar/fetch_goldbar.git"

2. Go into the directory: 
    
        cd fetch_goldbar

3. Build Docker Image: (It might take some time to build this.)

        docker build -t goldbar-app .

4. Run the docker container:

        docker run -it --name mygoldbarapp goldbar-app

    If you want to also run the unit tests. 

        docker run -it --name mygoldbarapp goldbar-app bash

5. Inside the bash run the testfiles. 

        pytest testfiles 

6. I have predefined the bar values. If you want you can change it in the config.json. 

    If you want to edit config.json:

    First, install nano inside the docker container

        apt install nano

    Then Open the config.json in the nano editor

        nano config.json

    Change the bar values. The Bar values should be unique in each bar. i.e. If you have entered 0, 1, 2 on the left, then these bars will not be present on the right and remaining. All the bar_lists should have a length of 3. The value of the bar should be between 0-8. 

    If these conditions are not satisfied, the code will raise a Value Error. 

7. Once configured, you can run the code using:

        python3 main.py

8. Exit and Stop the container.

        exit

    Display containers:
        
        docker ps -a

    If any container is running. 

        docker stop <container_id>
    
    If you want to remove the container

        docker rm <container id>
    
    If you want to display and delete an image:

        docker images
        docker rmi <image_id>


## Run without using docker. 

If you don't have docker or do not want to use docker. You can perform the following steps.

1. Install Google Chrome. 
2. Download ChromeDriver release compatible with your Google Chrome. 
3. Unzip ChromDriver and move it into usr/local/bin
3. Clone the repository and cd into the repository. 
4. Install venv and create a virtual environment:

        sudo apt install python3 python3-pip python3-venv
        python3 -m venv venv

5. source venv/bin/activate
6. pip install -r requirements.txt
7. Now run the code:

        python3 main.py

8. If your current running environment has GUI, you can also see the test running by changing the config.json. 

        In the config.json, change "isheadless" to 0.

    Note:  This won't work in docker, as the docker container doesn't have GUI. 

## File Structure:

-main.py: Initializes object of GoldBarWeighing and calls the required functions.
-app:
    - __init__.py
    - goldbar.py: Defines the GoldBarWeighing Class
    - web_driver_config.py: Defines Web Driver Class
    - web_driver_utilities.py: Defines Web Driver utility class functions like click button, set text
    - logger.py: Initializes logging
-testfiles: Unit test files
    - test_enter_bars_on_bowl.py
    - test_find_fake_bar.py
    - test_find_suspected_bars.py
    - test_print_weighings_list.py
    - test_validate_answer.py
    - test_weigh.py
    - test_valid_bar_value.py
-requirements.txt
-config.json: Options for headless, bar values, and url. 


## Code Overview:

I have defined the GoldBarWeighing Class with all the required methods.

GoldBarWeighing: This class manages the interaction with the balance scale web interface using Selenium WebDriver. It supports initializing a web session, conducting weighings, and determining the fake gold bar through systematic tests.

Functional Methods:

reset():
Resets the balance scale by clicking the reset button on the webpage. 

enter_bars_on_bowl():
Place specified bars on either the left or right side of the scale. 

weigh():
Conducts a weighing operation by placing the specified bars on the left and right sides of the scale and triggers the weighing process. It waits for the result and returns the outcome ('<', '>', '=') indicating which side is lighter or if both sides are balanced.

find_suspected_bars():
Identifies the likely group containing the fake bar based on the result of a weighing. 

valid_bar_value():
Validates if the bar values satisfy the required conditions. 

find_fake_bar():
Starts the process to determine the fake gold bar using a minimum of weighings. 

validate_answer():
Validates the identified fake bar by simulating a click on the respective bar's button on the web interface and interpreting the alert message to confirm if the selection is correct.

print_weighings_list():
Outputs the list of all weighings performed during the session, providing a trace of actions for review or debugging.

## Challenges:

1. While trying to reset the bowl grids, I realized that the ID of the reset button and the result button are the same. So I could not directly access it using By.ID, so I had to explore By.CSS_SELECTOR.

2. While creating the docker file, it was difficult to set up the chrome driver.
3. 
Overall this was a great challenge where I could implement my skills and also learn new concepts. 
