# Python wrapper for Stanford CoreNLP

1. Download [Stanford CoreNLP](http://stanfordnlp.github.io/CoreNLP/) and unpack it.
2. Download stanford-corenlp-python-wrapper:

    `git clone https://github.com/askmyhat/stanford-corenlp-python-wrapper`

3. Put StanfordCoreNLP.py from this repository in your project directory

<details> 
  <summary>Configuring OpenIE</summary>
There isn't prompt string in OpenIE shell so we have to add it.
Execute this in CoreNLP root to get sources:

    mkdir src
    cd src
    jar -xf ../stanford-corenlp-3.6.0-sources.jar 
    cd ..
    
Edit file `./src/edu/stanford/nlp/naturalli/OpenIE.java`:

```diff
    724     if (filesToProcess.length == 0) {
    725       // Running from stdin; one document per line.
-   726       System.err.println("Processing from stdin. Enter one sentence per line.");
+   726       System.err.println("NLP>");
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
+   738           System.err.println("NLP>");
    739           line = scanner.nextLine();
    740         } catch (NoSuchElementException e) {
    741           return;
    742         }
    743       }
```

Recompile CoreNLP

    ant
    cd classes
    jar -cfm ../stanford-corenlp-3.6.0.jar ../src/META-INF/MANIFEST.MF edu
    cd ..

</details>

### Usage example:

    import StanfordCoreNLP as nlp
    p = nlp.OpenIE()
    r = p.process(nlp.sample[1])
    print(r)
