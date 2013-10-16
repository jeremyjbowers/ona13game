      // ensure the web page (DOM) has loaded
      document.addEventListener("DOMContentLoaded", function () {

         // Create a popcorn instance by calling the Vimeo player plugin
         var example = Popcorn.vimeo(
         '#video',
         'http://player.vimeo.com/video/76991191');

         example.timeline({
          start: 1,
          target: "timeline",
          title: " ",
          text: " ",
          innerHTML:
          "<h3>ONA13 Music in Atlanta</h3><p>Welcome to ONA13!</p><p>Wondering how you're going to fill your nights in the A? Never fear! We're here to help with some great local shows and restaurants around town.</p>",
          direction: "up,"

         });
         //Ruby Velle & The Soulphonics
         example.timeline({
          start: 10,
          target: "timeline",
          title: " ",
          text: " ",
          innerHTML: "<h4>THURSDAY</h4><h2>ONA Presents:</h2><h1>Ruby Velle & The Soulphonics</h1>",
          direction: "up",
         });

         //Atlas Genius
         example.timeline({
          start: 19,
          target: "timeline",
          title: " ",
          text: " ",
          innerHTML: "<h4>THURSDAY</h4><h2>Atlas Genius</h2><h3>Center Stage Theater at 8:30</h3>",
          direction: "up",
         });

        //Wild Belle
        example.timeline({
          start: 33,
          target: "timeline",
          title: " ",
          text: " ",
          innerHTML: "<h4>THURSDAY</h4><h2>Wild Belle & Snowmine</h2><h3>The EARL at 9:00</h3>",
          direction: "up",
         });

        //Cherry Poppin Daddies
        example.timeline({
          start: 51,
          target: "timeline",
          title: " ",
          text: " ",
          innerHTML: "<h4>THURSDAY</h4><h2>Cherry Poppin Daddies</h2><h3>Smith's Olde Bar at 8:00</h3>",
          direction: "up",
         });
        //friday
        example.timeline({
          start: 67,
          target: "timeline",
          title: " ",
          text: " ",
          innerHTML: "<h1>FRIDAY</h4>",
          direction: "up",
         });
        //Larkin Poe
        example.timeline({
          start: 69,
          target: "timeline",
          title: " ",
          text: " ",
          innerHTML: "<h4>FRIDAY</h4><h2>Larkin Poe</h2><h3>Eddie's Attic at 7:00</h3>",
          direction: "up",
         });
        //The Whigs
        example.timeline({
          start: 89,
          target: "timeline",
          title: " ",
          text: " ",
          innerHTML: "<h4>FRIDAY</h4><h2>The Whigs</h2><h3>Terminal West at 9:00</h3>",
          direction: "up",
         });

        example.timeline({
          start: 102,
          target: "timeline",
          title: " ",
          text: " ",
          innerHTML: "<h4>FRIDAY</h4><h2>Patty Griffin</h2><h3>Buckhead Theatre at 8:00</h3>",
          direction: "up",
         });

        example.timeline({
          start: 112,
          target: "timeline",
          title: " ",
          text: " ",
          innerHTML: "<h4>FRIDAY</h4><h2>Ben Rector</h2><h3>Smith's Olde Bar at 8:00</h3>",
          direction: "up",
         });

        example.timeline({
          start: 127,
          target: "timeline",
          title: " ",
          text: " ",
          innerHTML: "<h1>SATURDAY</h1>",
          direction: "up",
         });

        example.timeline({
          start: 129,
          target: "timeline",
          title: " ",
          text: " ",
          innerHTML: "<h4>SATRDAY</h4><h2>Guitar Wolf</h2><h3>Drunken Unicorn at 9:00</h3>",
          direction: "up",
         });

        example.timeline({
          start: 139,
          target: "timeline",
          title: " ",
          text: " ",
          innerHTML: "<h4>SATURDAY</h4><h2>Lucius</h2><h3>The EARL at 8:00</h3>",
          direction: "up",
         });

        example.timeline({
          start: 155,
          target: "timeline",
          title: " ",
          text: " ",
          innerHTML: "<h4>SATURDAY</h4><h2>Todd Carey</h2><h3>Smith's Olde Bar at 8:00</h3>",
          direction: "up",
         });


        example.timeline({
          start: 167,
          target: "timeline",
          title: " ",
          text: " ",
          innerHTML: "<h1>SUNDAY</h1>",
          direction: "up",
         });

        example.timeline({
          start: 169,
          target: "timeline",
          title: " ",
          text: " ",
          innerHTML: "<h4>SUNDAY</h4><h2>Kris Kristofferson</h2><h3>Atlanta Symphony Hall at 7:30</h3>",
          direction: "up",
         });

        example.timeline({
          start: 180,
          target: "timeline",
          title: " ",
          text: " ",
          innerHTML: "<h4>SUNDAY</h4><h2>Grupo Fantasma</h2><h3>The EARL at 8:00</h3>",
          direction: "up",
         });

        example.timeline({
          start: 195,
          target: "timeline",
          title: " ",
          text: " ",
          innerHTML: "<h4>SUNDAY</h4><h2>Poor Old Shine</h2><h3>Eddie's Attic at 8:00</h3>",
          direction: "up",
         });

        //});


         // .timeline({
         //  start: 33,
         // })

         // .timeline({
         //  start: 51,
         // })

         // .timeline({

         // })

         // add a footnote at 2 seconds, and remove it at 6 seconds
         // example.footnote({
         //   start: 2,
         //   end: 6,
         //   text: "Pop!",
         //   target: "footnotediv"
         // });

         // play the video right away
         example.play();

      }, false);