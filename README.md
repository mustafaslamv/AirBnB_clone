# 0x00. AirBnB clone - The console

<div style="background-color: white;">
  ![AirBnB Clone](hbnb.png)
</div>

This is the first step towards building my first full web application: the AirBnB clone

## The console uses:

- create data model
- manage (create, update, destroy, etc) objects via a console / command interpreter
- store and persist objects to a file (JSON file)


<h3>Execution</h3>

<pre><code>$ ./console.py
(hbnb) help

Documented commands (type help &lt;topic&gt;):
========================================
EOF  help  quit

(hbnb)
(hbnb)
(hbnb) quit
$
</code></pre>

<p>But also in non-interactive mode: (like the Shell project in C)</p>

<pre><code>$ echo "help" | ./console.py
(hbnb)

Documented commands (type help &lt;topic&gt;):
========================================
EOF  help  quit
(hbnb)
$
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)

Documented commands (type help &lt;topic&gt;):
========================================
EOF  help  quit
(hbnb)
$
</code></pre>
