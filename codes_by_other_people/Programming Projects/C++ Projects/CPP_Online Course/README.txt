The directory structure is set up for Code::Blocks with GCC 4.4 which is currently experimental. Unzip directly into the root C:\.

I have not been testing the programs with 4.3.2 (the current official release though most
should be fine).

AllPrograms.workspace will load all of the Projects to allow all programs in the book to be
rebuilt at once.

TestApp is a special project which I use to check new '09 features that are not currently
implemented. At the beginning of the file is a #define TRYx with a short explanation of the feature.
Uncomment the #define and compile the project to see if it's working (yet). If you get an error
message, then the feature probably isn't supported yet. TestApp will not ship with the book.

TestAppn are projects that I create to test out features. They will not ship with the book.
