import os, sys

if len(sys.argv) == 1 or sys.argv[1] == 'build-lewi':
    os.system("javac -classpath jlewi/src/java/:jlewi/lib/commons-lang3-3.13.0.jar jlewi/src/java/swisseph/*.java")
    os.system("javac -classpath jlewi/src/java/:jlewi/lib/commons-lang3-3.13.0.jar jlewi/src/java/org/jlewi/*.java")
    
if len(sys.argv) == 1 or sys.argv[1] == 'jar':
    os.system("jar cmvf META-INF/MANIFEST.MF astromaestro.jar -C jlewi/src/java .")

if len(sys.argv) == 1 or sys.argv[1] == 'gen-decans':
    os.system("java -classpath jlewi/lib/commons-lang3-3.13.0.jar:astromaestro.jar org.jlewi.GenerateDecans")

if len(sys.argv) == 1 or sys.argv[1] == 'test-vedic':
    os.system("java -classpath jlewi/lib/commons-lang3-3.13.0.jar:astromaestro.jar swisseph.VedicTest")

if len(sys.argv) == 1 or sys.argv[1] == 'test-vedic2':
    os.system("java -classpath jlewi/lib/commons-lang3-3.13.0.jar:astromaestro.jar swisseph.Vedic")

if len(sys.argv) == 1 or sys.argv[1] == 'gen-combined':
    import astromaestro
    astromaestro.gen_combined()
    
