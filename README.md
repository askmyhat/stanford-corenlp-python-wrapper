# stanford-corenlp-python-wrapper
Functions for using Stanford CoreNLP through python

Download [Stanford NLP](http://stanfordnlp.github.io/CoreNLP/) and unpack it

If you want to use OpenIE you have to add printing prompt string code in it's source.

<details> 
  <summary>Instruction for UNIX</summary>
Run this commands in CoreNLP root to get sources:

    mkdir src
    cd src
    jar -xf ../stanford-corenlp-3.6.0-sources.jar 
    cd ..
    
Then open file `./src/edu/stanford/nlp/naturalli/OpenIE.java` find following block of code and insert one more line.

```diff
    724     if (filesToProcess.length == 0) {
    725       // Running from stdin; one document per line.
    726       System.err.println("Processing from stdin. Enter one sentence per line.");
    727       Scanner scanner = new Scanner(System.in);
    728       String line;
    729       try {
    730         line = scanner.nextLine();
    731       } catch (NoSuchElementException e) {
    732         System.err.println("No lines found on standard in");
    733         return;
    734       }
    735       while (line != null) {
    736         processDocument(pipeline, "stdin", line);
    737         try {
+   738           System.err.println("OpenIE> ");
    739           line = scanner.nextLine();
    740         } catch (NoSuchElementException e) {
    741           return;
    742         }
    743       }
```

Now recompile CoreNLP

    ant
    cd classes
    jar -cfm ../stanford-corenlp-3.6.0.jar ../src/META-INF/MANIFEST.MF edu
    cd ..

</details>
