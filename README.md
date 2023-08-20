<h1>CPP Junk Code Py</h1>

<h2>Desc</h2>
<p>Nothing mental, avoid signature based detection and annoy anyone reversing your codes. Currenttly uses https://junkcode.gehaxelt.in/ to generate large classes. 
However I want to make this fully offline as I update the script</p>

<h2>Usage</h2>
<p>Will be adding arguments soon. Insert your cpp files into the root directory with the script, the script will parse each file for your specified macros and insert 
junk code in their place. All new files are created in ./parsed directory. Original code is left untouched.</p>
<p>At present the macro you choose to use for junk code should only be placed inside of functions as it uses loops but it future updates I will fix this and add some further configuartion options.</p>

<h2>Plans</h2>
<ul>
  <li>Improve variable generation</li>
  <li>Loop diversity</li>
  <li>Jmps / skips to completley subtly skip the code at runtime</li>
  <li>Command line args / better usability for better integration</li>
  <li>Further optimisations</li>
  <li>Full build integration</li>
</ul>
