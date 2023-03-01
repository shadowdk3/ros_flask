#! /usr/bin/env python

import threading

from flask import Flask, render_template, request

import rospy
from geometry_msgs.msg import Twist

threading.Thread(target=lambda: rospy.init_node('web_server', disable_signals=True)).start()

cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

app = Flask(__name__,
    static_url_path='', 
    static_folder='static',
    template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        element_name = request.form['name']

        if element_name == "joy1Div":
            joy_x = float(request.form['joy_x']) / 100.
            joy_y = float(request.form['joy_y']) / 100.


            """
            x, z
                ++  | +-
                ----------
                --  | -+
            """

            cmd_vel = Twist()
            cmd_vel.linear.x = joy_y
            cmd_vel.angular.z = joy_x

            cmd_vel_pub.publish(cmd_vel)

            return {"joy_x" : joy_x, "joy_y" : joy_y}

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6688)
