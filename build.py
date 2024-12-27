import os, sys

if sys.argv[1] == 'compile':
    os.system("javac -classpath jlewi/src/java/:jlewi/lib/commons-lang3-3.13.0.jar jlewi/src/java/swisseph/*.java")
    os.system("javac -classpath jlewi/src/java/:jlewi/lib/commons-lang3-3.13.0.jar jlewi/src/java/org/jlewi/*.java")
    
if sys.argv[1] == 'jar':
    os.system("jar cmvf META-INF/MANIFEST.MF astromaestro.jar -C jlewi/src/java .")

if sys.argv[1] == 'gen-decans':
    os.system("java -classpath jlewi/lib/commons-lang3-3.13.0.jar:astromaestro.jar org.jlewi.GenerateDecans")

if sys.argv[1] == 'test-vedic':
    os.system("java -classpath jlewi/lib/commons-lang3-3.13.0.jar:astromaestro.jar swisseph.VedicTest")

if sys.argv[1] == 'test-vedic2':
    os.system("java -classpath jlewi/lib/commons-lang3-3.13.0.jar:astromaestro.jar swisseph.Vedic 1 10 1963 10 10 10 1")

if sys.argv[1] == 'gen-combined':
    import astromaestro
    astromaestro.gen_combined()
    
if sys.argv[1] == 'zip':
    os.system("zip /opt/Downloads/dotbkps/astromaestro.zip -r /home/burak/Documents/repos/astromaestro/.git/")
