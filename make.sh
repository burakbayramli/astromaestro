rm /tmp/astclasses/*.class
javac -d /tmp/astclasses -classpath jlewi/src/java/:jlewi/lib/commons-lang3-3.13.0.jar Combined3.java
java -classpath /tmp/astclasses:jlewi/lib/commons-lang3-3.13.0.jar VedicTest
java -classpath /tmp/astclasses:jlewi/lib/commons-lang3-3.13.0.jar DecanTest
