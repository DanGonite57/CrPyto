from string import whitespace


def remove(text):
    return ''.join(char for char in text if char not in whitespace)

#print(remove("""THE SIGNS WERE SUBTLE, AND IT TOOK ME A WHILE TO SPOT THEM, BUT GRADUALLY I STARTED TO MAKE THEM OUT, AND LIKE ONE OF THOSE OLD FASHIONED 3D PICTURES, THAT SPRINGS INTO FOCUS WHEN YOU CROSS YOUR EYES AND COUNT TO A HUNDRED, THE TRUTH CRYSTALLISED AND I REALISED THAT I HAD BEEN SEARCHING FOR IT ALL ALONG. IT WASN’T THAT I FOUND SOMETHING PARTICULAR. WHAT I NOTICED WAS ACTUALLY AN ABSENCE, A WHOLE COLLECTION OF APPARENTLY UNRELATED THINGS THAT SHOULD HAVE EXISTED BUT DIDN’T. AND JUST AS I HAD FIGURED THAT OUT, SOMEONE, AND BACK THEN I DIDN’T KNOW WHO, WROTE TO TELL ME ABOUT IT. THEY OBVIOUSLY HAD A SENSE OF THE DRAMATIC, AND AN EXCELLENT SENSE OF TIMING. IF THEY HAD SENT IT TO ME EVEN A FEW DAYS BEFORE I WOULD HAVE ASSUMED IT WAS SOME KIND OF CRAZY ADVERTISING STUNT, BUT WHEN THE POSTCARD ARRIVED, IT WAS IMMEDIATELY OBVIOUS TO ME WHAT IT REFERRED TO. IT CARRIED JUST THREE WORDS, AND IT DESCRIBED PERFECTLY THE MISSING PIECES IN MY PUZZLE. IT JUST SAID: THE SHADOW ARCHIVE."""))