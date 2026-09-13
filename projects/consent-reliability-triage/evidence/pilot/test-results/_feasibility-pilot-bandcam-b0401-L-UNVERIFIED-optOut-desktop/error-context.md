# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: _feasibility-pilot.spec.ts >> bandcamp.com >> bandcamp.com 85db .LOCAL_UNVERIFIED optOut desktop
- Location: playwright/runner.ts:361:21

# Error details

```
Error: selfTestResult received, but failed

expect(received).toBe(expected) // Object.is equality

Expected: true
Received: false
```

# Page snapshot

```yaml
- generic [ref=e3]:
  - link "Skip to content" [ref=e4] [cursor=pointer]:
    - /url: "#content"
  - banner [ref=e6]:
    - navigation "Bandcamp" [ref=e7]:
      - menubar "Main menu" [ref=e8]:
        - menuitem "Bandcamp home" [ref=e9] [cursor=pointer]:
          - img [ref=e10]
          - generic [ref=e13]: Bandcamp home
        - menuitem [ref=e14]:
          - search [ref=e15]:
            - generic [ref=e16]:
              - generic [ref=e17]: Search for artist, album or track
              - searchbox "Search for artist, album or track" [ref=e19]
            - button "Search" [ref=e20] [cursor=pointer]
        - menuitem "Sign up" [ref=e21] [cursor=pointer]
        - menuitem "Log in" [ref=e22] [cursor=pointer]
    - navigation [ref=e23]:
      - menubar "Page navigation" [ref=e24]:
        - menuitem "Digital music" [ref=e25] [cursor=pointer]:
          - img [ref=e26]
          - text: Digital music
        - menuitem "Vinyl" [ref=e28] [cursor=pointer]:
          - img [ref=e29]
          - text: Vinyl
        - menuitem "Compact discs" [ref=e34] [cursor=pointer]:
          - img [ref=e35]
          - text: Compact discs
        - menuitem "Cassettes" [ref=e38] [cursor=pointer]:
          - img [ref=e39]
          - text: Cassettes
        - menuitem "T-shirts" [ref=e44] [cursor=pointer]:
          - img [ref=e45]
          - text: T-shirts
        - menuitem "Gift cards" [ref=e47] [cursor=pointer]:
          - img [ref=e48]
          - text: Gift cards
        - menuitem "Editorial" [ref=e51] [cursor=pointer]:
          - img [ref=e52]
          - text: Editorial
        - menuitem "Radio" [ref=e54] [cursor=pointer]:
          - img [ref=e55]
          - text: Radio
  - main [ref=e59]:
    - generic [ref=e61]:
      - heading "Fans have paid artists $1.8 billion using Bandcamp, and yesterday alone bought 86,925 records." [level=1] [ref=e62]:
        - text: Fans have paid artists
        - mark [ref=e63]: $1.8 billion
        - text: using Bandcamp, and yesterday alone bought
        - mark [ref=e64]: 86,925
        - text: records.
      - generic [ref=e65]:
        - img [ref=e66]
        - img [ref=e68]
        - img [ref=e70]
      - generic [ref=e72]:
        - img [ref=e73]
        - img [ref=e75]
    - generic [ref=e80]:
      - generic [ref=e81]:
        - generic [ref=e82]: selling right now
        - button "pause" [ref=e83] [cursor=pointer]
      - generic [ref=e84]:
        - list [ref=e86]:
          - listitem [ref=e87]:
            - link "Messages From The Stars Sold for £1.20 ·5 seconds ago" [ref=e88] [cursor=pointer]:
              - /url: https://therahband.bandcamp.com/track/messages-from-the-stars?from=salesfeed
              - img "Messages From The Stars" [ref=e90]
              - strong [ref=e92]: Sold for £1.20
              - time [ref=e94]: ·5 seconds ago
          - listitem [ref=e95]:
            - link "Always Moving Forward Sold for $2 ·6 seconds ago" [ref=e96] [cursor=pointer]:
              - /url: https://annakarina.bandcamp.com/album/always-moving-forward?from=salesfeed
              - img "Always Moving Forward" [ref=e98]
              - strong [ref=e100]: Sold for $2
              - time [ref=e102]: ·6 seconds ago
          - listitem [ref=e103]:
            - link "Beyond Obsidian Euphoria Sold for $10 ·8 seconds ago" [ref=e104] [cursor=pointer]:
              - /url: https://tomarum.bandcamp.com/album/beyond-obsidian-euphoria?from=salesfeed
              - img "Beyond Obsidian Euphoria" [ref=e106]
              - strong [ref=e108]: Sold for $10
              - time [ref=e110]: ·8 seconds ago
          - listitem [ref=e111]:
            - link "Ash in Realms of Stone Icons Sold for $12 ·8 seconds ago" [ref=e112] [cursor=pointer]:
              - /url: https://tomarum.bandcamp.com/album/ash-in-realms-of-stone-icons?from=salesfeed
              - img "Ash in Realms of Stone Icons" [ref=e114]
              - strong [ref=e116]: Sold for $12
              - time [ref=e118]: ·8 seconds ago
          - listitem [ref=e119]:
            - link "Chat Pile \"Dragonslayer\" Citrine Shirt Sold for $35 ·9 seconds ago" [ref=e120] [cursor=pointer]:
              - /url: https://chatpile.bandcamp.com/merch/chat-pile-dragonslayer-citrine-shirt?from=salesfeed
              - img "Chat Pile \"Dragonslayer\" Citrine Shirt" [ref=e122]
              - strong [ref=e124]: Sold for $35
              - time [ref=e126]: ·9 seconds ago
          - listitem [ref=e127]:
            - link "The Sea of Tragic Beasts Sold for $11 ·12 seconds ago" [ref=e128] [cursor=pointer]:
              - /url: https://fitforanautopsy.bandcamp.com/album/the-sea-of-tragic-beasts?from=salesfeed
              - img "The Sea of Tragic Beasts" [ref=e130]
              - strong [ref=e132]: Sold for $11
              - time [ref=e134]: ·12 seconds ago
          - listitem [ref=e135]:
            - 'link "PICTURA DE IPSE : Musique directe Sold for $12 CAD ·15 seconds ago" [ref=e136] [cursor=pointer]':
              - /url: https://hubertlenoir.bandcamp.com/album/pictura-de-ipse-musique-directe?from=salesfeed
              - 'img "PICTURA DE IPSE : Musique directe" [ref=e138]'
              - strong [ref=e140]: Sold for $12 CAD
              - time [ref=e142]: ·15 seconds ago
          - listitem [ref=e143]:
            - link "A Diamond For Disease Sold for $8.99 ·17 seconds ago" [ref=e144] [cursor=pointer]:
              - /url: https://arsis.bandcamp.com/album/a-diamond-for-disease?from=salesfeed
              - img "A Diamond For Disease" [ref=e146]
              - strong [ref=e148]: Sold for $8.99
              - time [ref=e150]: ·17 seconds ago
          - listitem [ref=e151]:
            - link "Social Living Sold for $10 ·22 seconds ago" [ref=e152] [cursor=pointer]:
              - /url: https:https://bandcamp.gum.studio/album/social-living?from=salesfeed
              - img "Social Living" [ref=e154]
              - strong [ref=e156]: Sold for $10
              - time [ref=e158]: ·22 seconds ago
          - listitem [ref=e159]:
            - link "Not For You Sold for $5 ·25 seconds ago" [ref=e160] [cursor=pointer]:
              - /url: https://selfabsorbed.bandcamp.com/album/not-for-you?from=salesfeed
              - img "Not For You" [ref=e162]
              - strong [ref=e164]: Sold for $5
              - time [ref=e166]: ·25 seconds ago
          - listitem [ref=e167]:
            - link "ARTSTRANSP016 // 12\" VINYL Tie & Die Black White in ARTS Sleeve Sold for €12.75 ·25 seconds ago" [ref=e168] [cursor=pointer]:
              - /url: https://artsrecordings.bandcamp.com/album/antiquated-thoughts-ep?from=salesfeed
              - img "ARTSTRANSP016 // 12\" VINYL Tie & Die Black White in ARTS Sleeve" [ref=e170]
              - strong [ref=e172]: Sold for €12.75
              - time [ref=e174]: ·25 seconds ago
          - listitem [ref=e175]:
            - link "Wedding, Funeral Sold for $1 ·25 seconds ago" [ref=e176] [cursor=pointer]:
              - /url: https://waitresscore.bandcamp.com/track/wedding-funeral?from=salesfeed
              - img "Wedding, Funeral" [ref=e178]
              - strong [ref=e180]: Sold for $1
              - time [ref=e182]: ·25 seconds ago
          - listitem [ref=e183]:
            - link "The Very Thing That You Hate Sold for $1 ·25 seconds ago" [ref=e184] [cursor=pointer]:
              - /url: https://waitresscore.bandcamp.com/track/the-very-thing-that-you-hate?from=salesfeed
              - img "The Very Thing That You Hate" [ref=e186]
              - strong [ref=e188]: Sold for $1
              - time [ref=e190]: ·25 seconds ago
          - listitem [ref=e191]:
            - link "Stealing the Keys to the Time Machine Sold for $1 ·25 seconds ago" [ref=e192] [cursor=pointer]:
              - /url: https://waitresscore.bandcamp.com/track/stealing-the-keys-to-the-time-machine?from=salesfeed
              - img "Stealing the Keys to the Time Machine" [ref=e194]
              - strong [ref=e196]: Sold for $1
              - time [ref=e198]: ·25 seconds ago
          - listitem [ref=e199]:
            - link "Here Come The Cats Sold for $2 ·25 seconds ago" [ref=e200] [cursor=pointer]:
              - /url: https://waitresscore.bandcamp.com/track/here-come-the-cats?from=salesfeed
              - img "Here Come The Cats" [ref=e202]
              - strong [ref=e204]: Sold for $2
              - time [ref=e206]: ·25 seconds ago
          - listitem [ref=e207]:
            - link "Connie Sold for $1 ·25 seconds ago" [ref=e208] [cursor=pointer]:
              - /url: https://waitresscore.bandcamp.com/track/connie?from=salesfeed
              - img "Connie" [ref=e210]
              - strong [ref=e212]: Sold for $1
              - time [ref=e214]: ·25 seconds ago
        - text: · · · · · · · · · · · · · · · ·
    - region "Bandcamp Daily" [ref=e215]:
      - generic [ref=e216]:
        - generic [ref=e217]:
          - heading "Bandcamp Daily" [level=2] [ref=e219]
          - generic [ref=e220]:
            - paragraph [ref=e222]: Read articles on the latest releases, learn about niche genres, and explore global music scenes.
            - link "Explore more editorial" [ref=e223] [cursor=pointer]:
              - /url: https://daily.bandcamp.com/?from=homepage&ui_context=featured_editorial
        - generic [ref=e224]:
          - generic [ref=e225]:
            - link [ref=e226] [cursor=pointer]:
              - /url: https://daily.bandcamp.com/essential-releases/essential-releases-september-11-2026?from=homepage&ui_context=featured_editorial
            - generic [ref=e227]:
              - paragraph [ref=e228]: September 11, 2026
              - link "Essential Releases, September 11, 2026" [ref=e229] [cursor=pointer]:
                - /url: https://daily.bandcamp.com/essential-releases/essential-releases-september-11-2026?from=homepage&ui_context=featured_editorial
                - paragraph [ref=e230]: Essential Releases, September 11, 2026
              - paragraph [ref=e231]: Glitch pop, old time music, hip-hop, and more.
              - paragraph [ref=e232]: by Bandcamp Daily Staff
          - generic [ref=e233]:
            - generic [ref=e234]:
              - link [ref=e235] [cursor=pointer]:
                - /url: https://daily.bandcamp.com/scene-report/greenland-music-scene-report?from=homepage&ui_context=featured_editorial
              - link "It’s Not Easy Being Greenland" [ref=e237] [cursor=pointer]:
                - /url: https://daily.bandcamp.com/scene-report/greenland-music-scene-report?from=homepage&ui_context=featured_editorial
                - paragraph [ref=e238]: It’s Not Easy Being Greenland
            - generic [ref=e239]:
              - link [ref=e240] [cursor=pointer]:
                - /url: https://daily.bandcamp.com/big-ups/sylvan-esso-bandcamp-favorite-albums?from=homepage&ui_context=featured_editorial
              - link "Sylvan Esso Pick Their Bandcamp Favorites" [ref=e242] [cursor=pointer]:
                - /url: https://daily.bandcamp.com/big-ups/sylvan-esso-bandcamp-favorite-albums?from=homepage&ui_context=featured_editorial
                - paragraph [ref=e243]: Sylvan Esso Pick Their Bandcamp Favorites
            - generic [ref=e244]:
              - link [ref=e245] [cursor=pointer]:
                - /url: https://daily.bandcamp.com/features/solex-low-kick-and-hard-bop-album-guide?from=homepage&ui_context=featured_editorial
              - link "Solex Does It Again" [ref=e247] [cursor=pointer]:
                - /url: https://daily.bandcamp.com/features/solex-low-kick-and-hard-bop-album-guide?from=homepage&ui_context=featured_editorial
                - paragraph [ref=e248]: Solex Does It Again
    - region "Playlists in fan collections" [ref=e252]:
      - generic [ref=e253]:
        - generic [ref=e254]:
          - generic [ref=e255]:
            - heading "Playlists in fan collections" [level=2] [ref=e256]
            - generic [ref=e257]:
              - button "Prev" [disabled] [ref=e258] [cursor=pointer]:
                - img [ref=e259]
              - button "Next" [ref=e262] [cursor=pointer]:
                - img [ref=e263]
          - generic [ref=e266]:
            - paragraph [ref=e268]: Discover playlists curated by fans.
            - link "Learn more about playlists" [ref=e269] [cursor=pointer]:
              - /url: https://bandcamp.com/about_playlists?from=homepage&ui_context=whats_new
        - status [ref=e270]
        - list [ref=e271]:
          - listitem [ref=e272]:
            - group "1 of 12" [ref=e273]:
              - button "Play" [ref=e276] [cursor=pointer]:
                - img [ref=e277]
              - generic [ref=e280]:
                - link "Run as One 168 tracks, 12 hours 6 minutes" [ref=e282] [cursor=pointer]:
                  - /url: https://bandcamp.com/akeembalogun/playlist/run-as-one?from=homepage&ui_context=whats_new
                  - generic [ref=e283]: Run as One
                  - generic [ref=e284]: 168 tracks, 12 hours 6 minutes
                - paragraph [ref=e285]: All styles of grime, dark garage, real dubstep music and everything else in-between. These tracks fuel countless runs, but this isn't just a playlist to pound the ground to; have a listen for whatever purposes whenever.
                - generic [ref=e286]:
                  - img "Profile image" [ref=e288]
                  - text: Akeem Balogun
          - listitem [ref=e289]:
            - group "2 of 12" [ref=e290]:
              - button "Play" [ref=e293] [cursor=pointer]:
                - img [ref=e294]
              - generic [ref=e297]:
                - link "ambient reading 232 tracks, 21 hours 46 minutes" [ref=e299] [cursor=pointer]:
                  - /url: https://bandcamp.com/funkentechno/playlist/ambient-reading?from=homepage&ui_context=whats_new
                  - generic [ref=e300]: ambient reading
                  - generic [ref=e301]: 232 tracks, 21 hours 46 minutes
                - generic [ref=e302]:
                  - img "Profile image" [ref=e304]
                  - text: David James
          - listitem [ref=e305]:
            - group "3 of 12" [ref=e306]:
              - button "Play" [ref=e309] [cursor=pointer]:
                - img [ref=e310]
              - generic [ref=e313]:
                - link "south paw 22 tracks, 1 hour 23 minutes" [ref=e315] [cursor=pointer]:
                  - /url: https://bandcamp.com/robbie/playlist/south-paw?from=homepage&ui_context=whats_new
                  - generic [ref=e316]: south paw
                  - generic [ref=e317]: 22 tracks, 1 hour 23 minutes
                - paragraph [ref=e318]: Humbly submitted every week without genre, other than kinda fun (25 June issue)
                - generic [ref=e319]:
                  - img "Profile image" [ref=e321]
                  - text: wrobbiescott
          - listitem [ref=e322]:
            - group "4 of 12" [ref=e323]:
              - button "Play" [ref=e326] [cursor=pointer]:
                - img [ref=e327]
              - generic [ref=e330]:
                - link "FolkMyLife 20 tracks, 1 hour 14 minutes" [ref=e332] [cursor=pointer]:
                  - /url: https://bandcamp.com/folkmylife_blog/playlist/folkmylife?from=homepage&ui_context=whats_new
                  - generic [ref=e333]: FolkMyLife
                  - generic [ref=e334]: 20 tracks, 1 hour 14 minutes
                - paragraph [ref=e335]: This is my “hidden gems” play list for Cambridge Folk Festival 2026 !!! Get swiping to find out my 20 best picks for the festival you might not of heard of. I hope you fall in love with something.
                - generic [ref=e336]:
                  - img "Profile image" [ref=e338]
                  - text: FolkMyLife
          - listitem [ref=e339]:
            - group "5 of 12" [ref=e340]:
              - button "Play" [ref=e343] [cursor=pointer]:
                - img [ref=e344]
              - generic [ref=e347]:
                - link "snorkeling music 50 tracks, 5 hours 13 minutes" [ref=e349] [cursor=pointer]:
                  - /url: https://bandcamp.com/slabman/playlist/snorkeling-music?from=homepage&ui_context=whats_new
                  - generic [ref=e350]: snorkeling music
                  - generic [ref=e351]: 50 tracks, 5 hours 13 minutes
                - paragraph [ref=e352]: Immersive yet shallow; fun until it’s not. Was the water this hot last year?
                - generic [ref=e353]:
                  - img "Profile image" [ref=e355]
                  - text: misunderstander
          - listitem [ref=e356]:
            - group "6 of 12" [ref=e357]:
              - button "Play" [ref=e360] [cursor=pointer]:
                - img [ref=e361]
              - generic [ref=e364]:
                - link "fly azure sky 20 tracks, 1 hour 18 minutes" [ref=e366] [cursor=pointer]:
                  - /url: https://bandcamp.com/djhaka/playlist/fly-azure-sky?from=homepage&ui_context=whats_new
                  - generic [ref=e367]: fly azure sky
                  - generic [ref=e368]: 20 tracks, 1 hour 18 minutes
                - paragraph [ref=e369]: “anything can happen in the next half hour!” - commander shore, stingray. a voyage across genre. a hike through moods.
                - generic [ref=e370]:
                  - img "Profile image" [ref=e372]
                  - text: djhaka
          - listitem [ref=e373]:
            - group "7 of 12" [ref=e374]:
              - button "Play" [ref=e377] [cursor=pointer]:
                - img [ref=e378]
              - generic [ref=e381]:
                - link "Reading Room 22 tracks, 1 hour 41 minutes" [ref=e383] [cursor=pointer]:
                  - /url: https://bandcamp.com/ocean_everything/playlist/reading-room?from=homepage&ui_context=whats_new
                  - generic [ref=e384]: Reading Room
                  - generic [ref=e385]: 22 tracks, 1 hour 41 minutes
                - generic [ref=e386]:
                  - img "Profile image" [ref=e388]
                  - text: ocean_everything
          - listitem [ref=e389]:
            - group "8 of 12" [ref=e390]:
              - button "Play" [ref=e393] [cursor=pointer]:
                - img [ref=e394]
              - generic [ref=e397]:
                - link "Skeleton Mage & Other Projects 21 tracks, 1 hour 23 minutes" [ref=e399] [cursor=pointer]:
                  - /url: https://bandcamp.com/skeletonmage/playlist/skeleton-mage-other-projects?from=homepage&ui_context=whats_new
                  - generic [ref=e400]: Skeleton Mage & Other Projects
                  - generic [ref=e401]: 21 tracks, 1 hour 23 minutes
                - paragraph [ref=e402]: Songs by Skeleton Mage and my other Dungeon Synth projects.
                - generic [ref=e403]:
                  - img "Profile image" [ref=e405]
                  - text: Miguel Amarok
          - listitem [ref=e406]:
            - group "9 of 12" [ref=e407]:
              - button "Play" [ref=e410] [cursor=pointer]:
                - img [ref=e411]
              - generic [ref=e414]:
                - link "Canadian Post Punk 16 tracks, 58 minutes" [ref=e416] [cursor=pointer]:
                  - /url: https://bandcamp.com/charlesawesome/playlist/canadian-post-punk?from=homepage&ui_context=whats_new
                  - generic [ref=e417]: Canadian Post Punk
                  - generic [ref=e418]: 16 tracks, 58 minutes
                - generic [ref=e419]:
                  - img "Profile image" [ref=e421]
                  - text: Joey Fishman
          - listitem [ref=e422]:
            - group "10 of 12" [ref=e423]:
              - button "Play" [ref=e426] [cursor=pointer]:
                - img [ref=e427]
              - generic [ref=e430]:
                - link "Defrostatica Offroad 14 tracks, 1 hour 10 minutes" [ref=e432] [cursor=pointer]:
                  - /url: https://bandcamp.com/djbooga/playlist/defrostatica-offroad?from=homepage&ui_context=whats_new
                  - generic [ref=e433]: Defrostatica Offroad
                  - generic [ref=e434]: 14 tracks, 1 hour 10 minutes
                - paragraph [ref=e435]: "Defrostatica has specialized in releasing footwork jungle tekno. Here, we celebrate the outliers: from electro, breaks to house."
                - generic [ref=e436]:
                  - img "Profile image" [ref=e438]
                  - text: DJ Booga
          - listitem [ref=e439]:
            - group "11 of 12" [ref=e440]:
              - button "Play" [ref=e443] [cursor=pointer]:
                - img [ref=e444]
              - generic [ref=e447]:
                - link "“no skips” top albums of 2025 31 tracks, 2 hours 17 minutes" [ref=e449] [cursor=pointer]:
                  - /url: https://bandcamp.com/ajf070287/playlist/no-skips-top-albums-of-2025?from=homepage&ui_context=whats_new
                  - generic [ref=e450]: “no skips” top albums of 2025
                  - generic [ref=e451]: 31 tracks, 2 hours 17 minutes
                - generic [ref=e452]:
                  - img "Profile image" [ref=e454]
                  - text: burnt reverb
          - listitem [ref=e455]:
            - group "12 of 12" [ref=e456]:
              - button "Play" [ref=e459] [cursor=pointer]:
                - img [ref=e460]
              - generic [ref=e463]:
                - 'link "Ramsgate Radio: The Bandcamp Show Ep.1 14 tracks, 50 minutes" [ref=e465] [cursor=pointer]':
                  - /url: https://bandcamp.com/lydia_ltung/playlist/ramsgate-radio-the-bandcamp-show-ep1?from=homepage&ui_context=whats_new
                  - generic [ref=e466]: "Ramsgate Radio: The Bandcamp Show Ep.1"
                  - generic [ref=e467]: 14 tracks, 50 minutes
                - paragraph [ref=e468]: "We dive deep into the world of Bandcamp to uncover a hugely eclectic range of music, from soundtracks, to glitch, to hip hop, to indie. Although the selections travel across the globe, we dedicate each episode to bring you the music that exists right under our noses. You’ll undoubtedly be surprised with just how many music treasures are right here on Ramsgate’s doorstep. Photo credit: Dean Scutt"
                - generic [ref=e469]:
                  - img "Profile image" [ref=e471]
                  - text: Ramsgate Radio
    - region "Bandcamp Radio" [ref=e472]:
      - generic [ref=e473]:
        - generic [ref=e474]:
          - generic [ref=e475]:
            - heading "Bandcamp Radio" [level=2] [ref=e476]
            - generic [ref=e477]:
              - button "Prev" [disabled] [ref=e478] [cursor=pointer]:
                - img [ref=e479]
              - button "Next" [ref=e482] [cursor=pointer]:
                - img [ref=e483]
          - generic [ref=e486]:
            - paragraph [ref=e488]: Tune in weekly to hear new music and artist interviews.
            - link "View all shows" [ref=e489] [cursor=pointer]:
              - /url: https://bandcamp.com/radio?from=homepage&ui_context=bcradio
        - status [ref=e490]
        - list [ref=e491]:
          - listitem [ref=e492]:
            - group "1 of 6" [ref=e493]:
              - generic [ref=e495]:
                - generic [ref=e496]:
                  - 'link "September 11, 2026 Di''Anno: Iron Maiden''s Lost Singer The Metal Show" [ref=e497] [cursor=pointer]':
                    - /url: https://bandcamp.com/radio?show=998&from=homepage&ui_context=bcradio
                    - generic [ref=e498]: September 11, 2026
                    - generic [ref=e499]: "Di'Anno: Iron Maiden's Lost Singer"
                    - generic [ref=e500]: The Metal Show
                  - button "Play" [ref=e503] [cursor=pointer]:
                    - img [ref=e504]
                - paragraph [ref=e506]: Filmmaker Wes Orshoski joins the show to talk about his new documentary about the late Iron Maiden singer Paul Di'Anno.
                - generic [ref=e508]:
                  - text: Hosted by
                  - link "Brad Sanders" [ref=e509] [cursor=pointer]:
                    - /url: https://daily.bandcamp.com/contributors/brad-sanders
                  - text: . Featuring
                  - link "Wes Orshoski" [ref=e510] [cursor=pointer]:
                    - /url: https://cleopatrarecords.bandcamp.com/album/dianno-iron-maidens-lost-singer
                  - text: .
          - listitem [ref=e511]:
            - group "2 of 6" [ref=e512]:
              - generic [ref=e514]:
                - generic [ref=e515]:
                  - link "September 9, 2026 Dkay.wav Bandcamp Electronic" [ref=e516] [cursor=pointer]:
                    - /url: https://bandcamp.com/radio?show=997&from=homepage&ui_context=bcradio
                    - generic [ref=e517]: September 9, 2026
                    - generic [ref=e518]: Dkay.wav
                    - generic [ref=e519]: Bandcamp Electronic
                  - button "Play" [ref=e522] [cursor=pointer]:
                    - img [ref=e523]
                - paragraph [ref=e525]: London-based DJ and producer Dkay.wav passes through to talk about his debut EP on Patterns.
                - generic [ref=e527]:
                  - text: Hosted by
                  - link "Emily Dust" [ref=e528] [cursor=pointer]:
                    - /url: https://bandcamp.com/emilydust
                  - text: . Featuring
                  - link "Dkay.wav" [ref=e529] [cursor=pointer]:
                    - /url: https://dkaywav.bandcamp.com/
                  - text: and
                  - link "Izzi." [ref=e530] [cursor=pointer]:
                    - /url: https://bandcamp.com/izzi_thein
          - listitem [ref=e531]:
            - group "3 of 6" [ref=e532]:
              - generic [ref=e534]:
                - generic [ref=e535]:
                  - link "September 8, 2026 corto.alto Bandcamp Selects" [ref=e536] [cursor=pointer]:
                    - /url: https://bandcamp.com/radio?show=993&from=homepage&ui_context=bcradio
                    - generic [ref=e537]: September 8, 2026
                    - generic [ref=e538]: corto.alto
                    - generic [ref=e539]: Bandcamp Selects
                  - button "Play" [ref=e542] [cursor=pointer]:
                    - img [ref=e543]
                - paragraph [ref=e545]: corto.alto joins Tina Edwards to celebrate the new album, Some Small Fortune
                - generic [ref=e547]:
                  - text: Hosted by
                  - link "Tina Edwards" [ref=e548] [cursor=pointer]:
                    - /url: https://bandcamp.com/tinaedwards
                  - text: . Featuring
                  - link "corto.alto" [ref=e549] [cursor=pointer]:
                    - /url: https://cortoalto.bandcamp.com/album/some-small-fortune
          - listitem [ref=e550]:
            - group "4 of 6" [ref=e551]:
              - generic [ref=e553]:
                - generic [ref=e554]:
                  - link "September 4, 2026 Don't Come To My House Sharing Your Location The Hip Hop Show" [ref=e555] [cursor=pointer]:
                    - /url: https://bandcamp.com/radio?show=990&from=homepage&ui_context=bcradio
                    - generic [ref=e556]: September 4, 2026
                    - generic [ref=e557]: Don't Come To My House Sharing Your Location
                    - generic [ref=e558]: The Hip Hop Show
                  - button "Play" [ref=e561] [cursor=pointer]:
                    - img [ref=e562]
                - paragraph [ref=e564]: Girl Talk, Michael Christmas & Chris Crack join the show to chat about their new EP, "Don't Come To My House Sharing Your Location." — colorful, detailed, and genuinely fun, built on bars and nonstop ish talking.
                - generic [ref=e566]:
                  - text: Hosted by
                  - link "Stoney Creation" [ref=e567] [cursor=pointer]:
                    - /url: https://stoneycreation.bandcamp.com/music
                  - text: . Featuring
                  - link "Girl Talk, Michael Christmas, & Chris Crack" [ref=e568] [cursor=pointer]:
                    - /url: https://girltalkmusic.bandcamp.com/album/dont-come-to-my-house-sharing-your-location
                  - text: .
          - listitem [ref=e569]:
            - group "5 of 6" [ref=e570]:
              - generic [ref=e572]:
                - generic [ref=e573]:
                  - link "September 2, 2026 This is Lorelei The Indie Show" [ref=e574] [cursor=pointer]:
                    - /url: https://bandcamp.com/radio?show=986&from=homepage&ui_context=bcradio
                    - generic [ref=e575]: September 2, 2026
                    - generic [ref=e576]: This is Lorelei
                    - generic [ref=e577]: The Indie Show
                  - button "Play" [ref=e580] [cursor=pointer]:
                    - img [ref=e581]
                - paragraph [ref=e583]: Nate Amos of This is Lorelei talks about "The Singer in My Band" plus we hear new tracks from Pardoner, The Drin, Dummy, and more.
                - generic [ref=e585]:
                  - text: Hosted by
                  - link "Mariana Timony" [ref=e586] [cursor=pointer]:
                    - /url: https://bandcamp.com/marianatimony
                  - text: . Featuring
                  - link "This is Lorelei" [ref=e587] [cursor=pointer]:
                    - /url: https://thisislorelei.bandcamp.com/
                  - text: .
          - listitem [ref=e588]:
            - group "6 of 6" [ref=e589]:
              - generic [ref=e591]:
                - generic [ref=e592]:
                  - link "August 31, 2026 Tee Lopes The Game Show" [ref=e593] [cursor=pointer]:
                    - /url: https://bandcamp.com/radio?show=995&from=homepage&ui_context=bcradio
                    - generic [ref=e594]: August 31, 2026
                    - generic [ref=e595]: Tee Lopes
                    - generic [ref=e596]: The Game Show
                  - button "Play" [ref=e599] [cursor=pointer]:
                    - img [ref=e600]
                - paragraph [ref=e602]: Tee Lopes takes us behind the music of "Denshattack!", one of 2026's most anticipated OSTs.
    - region "New and Notable" [ref=e603]:
      - generic [ref=e604]:
        - generic [ref=e605]:
          - generic [ref=e606]:
            - heading "New and Notable" [level=2] [ref=e607]
            - generic [ref=e608]:
              - button "Prev" [disabled] [ref=e609] [cursor=pointer]:
                - img [ref=e610]
              - button "Next" [ref=e613] [cursor=pointer]:
                - img [ref=e614]
          - paragraph [ref=e619]: Explore the latest music releases, hand-selected by the Bandcamp editorial team.
        - status [ref=e620]
        - list [ref=e621]:
          - listitem [ref=e622]:
            - group "1 of 10" [ref=e623]:
              - generic [ref=e624]:
                - generic: Funk
                - button "Play" [ref=e626] [cursor=pointer]:
                  - img [ref=e627]
              - generic [ref=e630]:
                - link "Let’s Name a Star on Friday Night by Middle Blue Weird Funk" [ref=e632] [cursor=pointer]:
                  - /url: https://middleblueweirdfunk.bandcamp.com/album/let-s-name-a-star-on-friday-night?from=homepage&ui_context=new_and_notable
                  - generic [ref=e633]: Let’s Name a Star on Friday Night
                  - generic [ref=e634]: by Middle Blue Weird Funk
                - paragraph [ref=e635]: Enjoy the restlessly creative energy of Brad Ferber's jammy, "weird funk" project.
          - listitem [ref=e636]:
            - group "2 of 10" [ref=e637]:
              - generic [ref=e638]:
                - generic: Ambient
                - button "Play" [ref=e640] [cursor=pointer]:
                  - img [ref=e641]
              - generic [ref=e644]:
                - link "Drift And Anchor by Samatha" [ref=e646] [cursor=pointer]:
                  - /url: https://kordelrecords.bandcamp.com/album/drift-and-anchor?from=homepage&ui_context=new_and_notable
                  - generic [ref=e647]: Drift And Anchor
                  - generic [ref=e648]: by Samatha
                - paragraph [ref=e649]: Lullabies about drifting emotions recorded through spontaneous layering and looping.
          - listitem [ref=e650]:
            - group "3 of 10" [ref=e651]:
              - generic [ref=e652]:
                - generic: Alternative
                - button "Play" [ref=e654] [cursor=pointer]:
                  - img [ref=e655]
              - generic [ref=e658]:
                - link "Before Game Changer, I Broke Free From The Chains Of The Love Song by plainhead" [ref=e660] [cursor=pointer]:
                  - /url: https://plainhead.bandcamp.com/album/before-game-changer-i-broke-free-from-the-chains-of-the-love-song?from=homepage&ui_context=new_and_notable
                  - generic [ref=e661]: Before Game Changer, I Broke Free From The Chains Of The Love Song
                  - generic [ref=e662]: by plainhead
                - paragraph [ref=e663]: An EP of indietronica love songs from this Munich group prioritizes sweet melodies and earnest feelings.
          - listitem [ref=e664]:
            - group "4 of 10" [ref=e665]:
              - generic [ref=e666]:
                - generic: Pop
                - button "Play" [ref=e668] [cursor=pointer]:
                  - img [ref=e669]
              - generic [ref=e672]:
                - link "The Singer in My Band by This is Lorelei" [ref=e674] [cursor=pointer]:
                  - /url: https://thisislorelei.bandcamp.com/album/the-singer-in-my-band?from=homepage&ui_context=new_and_notable
                  - generic [ref=e675]: The Singer in My Band
                  - generic [ref=e676]: by This is Lorelei
                - paragraph [ref=e677]: A guitar-forward singer-songwriter record influenced by the pithy humor of Warren Zevon and life on the road.
          - listitem [ref=e678]:
            - group "5 of 10" [ref=e679]:
              - button "Play" [ref=e682] [cursor=pointer]:
                - img [ref=e683]
              - generic [ref=e686]:
                - link "Lefto presents Jazz Cats volume 4 by Various Artists" [ref=e688] [cursor=pointer]:
                  - /url: https://sdbanrecords.bandcamp.com/album/lefto-presents-jazz-cats-volume-4?from=homepage&ui_context=new_and_notable
                  - generic [ref=e689]: Lefto presents Jazz Cats volume 4
                  - generic [ref=e690]: by Various Artists
                - paragraph [ref=e691]: 14 tracks showcasing the most exciting emerging voices in Belgian jazz.
          - listitem [ref=e692]:
            - group "6 of 10" [ref=e693]:
              - generic [ref=e694]:
                - generic: Electronic
                - button "Play" [ref=e696] [cursor=pointer]:
                  - img [ref=e697]
              - generic [ref=e700]:
                - 'link "DJ-Kicks: Djrum by Djrum" [ref=e702] [cursor=pointer]':
                  - /url: https://djrum.bandcamp.com/album/dj-kicks-djrum-2?from=homepage&ui_context=new_and_notable
                  - generic [ref=e703]: "DJ-Kicks: Djrum"
                  - generic [ref=e704]: by Djrum
                - paragraph [ref=e705]: The latest installment in the legendary DJ-Kicks series features picks from the genius Djrum, including The Raincoats & Venetian Snares.
          - listitem [ref=e706]:
            - group "7 of 10" [ref=e707]:
              - generic [ref=e708]:
                - generic: Punk
                - button "Play" [ref=e710] [cursor=pointer]:
                  - img [ref=e711]
              - generic [ref=e714]:
                - link "Libertine by Foreign Body" [ref=e716] [cursor=pointer]:
                  - /url: https://foreignbodynyc.bandcamp.com/album/libertine?from=homepage&ui_context=new_and_notable
                  - generic [ref=e717]: Libertine
                  - generic [ref=e718]: by Foreign Body
                - paragraph [ref=e719]: Hitting like a kick to the teeth, the new LP from Foreign Body is gnarly, nasty, and fantastic.
          - listitem [ref=e720]:
            - group "8 of 10" [ref=e721]:
              - generic [ref=e722]:
                - generic: Alternative
                - button "Play" [ref=e724] [cursor=pointer]:
                  - img [ref=e725]
              - generic [ref=e728]:
                - link "The Counting Game by Antietam" [ref=e730] [cursor=pointer]:
                  - /url: https://dromedaryrecords.bandcamp.com/album/the-counting-game?from=homepage&ui_context=new_and_notable
                  - generic [ref=e731]: The Counting Game
                  - generic [ref=e732]: by Antietam
                - paragraph [ref=e733]: Lovely, meandering instrumental post-rock (the original version) from this long-running group that’s dazzling in its beauty.
          - listitem [ref=e734]:
            - group "9 of 10" [ref=e735]:
              - generic [ref=e736]:
                - generic: Hip-Hop/Rap
                - button "Play" [ref=e738] [cursor=pointer]:
                  - img [ref=e739]
              - generic [ref=e742]:
                - link "A Heap Of Broken Images by Blue Sky Black Death" [ref=e744] [cursor=pointer]:
                  - /url: https://bsbd.bandcamp.com/album/a-heap-of-broken-images-5?from=homepage&ui_context=new_and_notable
                  - generic [ref=e745]: A Heap Of Broken Images
                  - generic [ref=e746]: by Blue Sky Black Death
                - paragraph [ref=e747]: A classic returns! The absolutely essential debut from Blue Sky Black Death gets a gorgeous luxe vinyl reissue for its 20th anniversary.
          - listitem [ref=e748]:
            - group "10 of 10" [ref=e749]:
              - generic [ref=e750]:
                - generic: Alternative
                - button "Play" [ref=e752] [cursor=pointer]:
                  - img [ref=e753]
              - generic [ref=e756]:
                - link "80s kids 2 (2026) by Shannon Curtis" [ref=e758] [cursor=pointer]:
                  - /url: https://shannoncurtis.bandcamp.com/album/80s-kids-2-2026?from=homepage&ui_context=new_and_notable
                  - generic [ref=e759]: 80s kids 2 (2026)
                  - generic [ref=e760]: by Shannon Curtis
                - paragraph [ref=e761]: Shannon Curtis puts a sizzling spin on ’80s classics from Pet Shop Boys, New Order, Cutting Crew, and more.
    - generic [ref=e763]:
      - region "Album of the Day" [ref=e764]:
        - generic [ref=e765]:
          - generic [ref=e766]:
            - generic [ref=e767]:
              - heading "Album of the Day" [level=2] [ref=e768]
              - generic [ref=e769]:
                - button "Prev" [disabled] [ref=e770] [cursor=pointer]:
                  - img [ref=e771]
                - button "Next" [ref=e774] [cursor=pointer]:
                  - img [ref=e775]
            - generic [ref=e778]:
              - paragraph [ref=e780]: A deeper dive on an album we love.
              - link "View more albums" [ref=e781] [cursor=pointer]:
                - /url: https://daily.bandcamp.com/album-of-the-day?from=homepage&ui_context=album_of_the_day
          - status [ref=e782]
          - list [ref=e783]:
            - listitem [ref=e784]:
              - group "1 of 10" [ref=e785]:
                - generic [ref=e786]:
                  - generic: Country
                - generic [ref=e787]:
                  - generic [ref=e788]:
                    - link "September 11, 2026 Angela Autumn, “Believer”" [ref=e789] [cursor=pointer]:
                      - /url: https://daily.bandcamp.com/album-of-the-day/angela-autumn-believer-review?from=homepage&ui_context=album_of_the_day
                      - generic [ref=e790]: September 11, 2026
                      - generic [ref=e791]: Angela Autumn, “Believer”
                    - button "Play" [ref=e794] [cursor=pointer]:
                      - img [ref=e795]
                  - paragraph [ref=e797]: Embracing everything from psych-rock to indie folk, "Rose of Appalachia" breaks out of the old-time music box.
                  - link "Written by Brad Sanders" [ref=e798] [cursor=pointer]:
                    - /url: https://daily.bandcamp.com/contributors/brad-sanders
            - listitem [ref=e799]:
              - group "2 of 10" [ref=e800]:
                - generic [ref=e801]:
                  - generic: Experimental
                - generic [ref=e802]:
                  - generic [ref=e803]:
                    - link "September 10, 2026 Nate Mercereau, “Fantastic Thoughts”" [ref=e804] [cursor=pointer]:
                      - /url: https://daily.bandcamp.com/album-of-the-day/nate-mercereau-fantastic-thoughts-review?from=homepage&ui_context=album_of_the_day
                      - generic [ref=e805]: September 10, 2026
                      - generic [ref=e806]: Nate Mercereau, “Fantastic Thoughts”
                    - button "Play" [ref=e809] [cursor=pointer]:
                      - img [ref=e810]
                  - paragraph [ref=e812]: L.A. post-jazz instrumentalist and Andre 3000 collaborator pivots to radiant prog fantasia.
                  - link "Written by Jim Allen" [ref=e813] [cursor=pointer]:
                    - /url: https://daily.bandcamp.com/contributors/jim-allen
            - listitem [ref=e814]:
              - group "3 of 10" [ref=e815]:
                - generic [ref=e816]:
                  - generic: Alternative
                - generic [ref=e817]:
                  - generic [ref=e818]:
                    - link "September 9, 2026 Vanishing Twin, “Archives”" [ref=e819] [cursor=pointer]:
                      - /url: https://daily.bandcamp.com/album-of-the-day/vanishing-twin-archives-review?from=homepage&ui_context=album_of_the_day
                      - generic [ref=e820]: September 9, 2026
                      - generic [ref=e821]: Vanishing Twin, “Archives”
                    - button "Play" [ref=e824] [cursor=pointer]:
                      - img [ref=e825]
                  - paragraph [ref=e827]: Yé-yé grooves collide with images of life and art in a gleaming Space-Age future on the London act's latest.
                  - link "Written by Jennifer Kelly" [ref=e828] [cursor=pointer]:
                    - /url: https://daily.bandcamp.com/contributors/jennifer-kelly
            - listitem [ref=e829]:
              - group "4 of 10" [ref=e830]:
                - generic [ref=e831]:
                  - generic: Hip-Hop/Rap
                - generic [ref=e832]:
                  - generic [ref=e833]:
                    - link "September 8, 2026 doseone, Wino Willy & Zetroc, “sighting”" [ref=e834] [cursor=pointer]:
                      - /url: https://daily.bandcamp.com/album-of-the-day/doseone-wino-willy-zetroc-sighting-review?from=homepage&ui_context=album_of_the_day
                      - generic [ref=e835]: September 8, 2026
                      - generic [ref=e836]: doseone, Wino Willy & Zetroc, “sighting”
                    - button "Play" [ref=e839] [cursor=pointer]:
                      - img [ref=e840]
                  - paragraph [ref=e842]: A horror film made without a single frame of celluloid.
                  - link "Written by Dusty Henry" [ref=e843] [cursor=pointer]:
                    - /url: https://daily.bandcamp.com/contributors/Dusty Henry
            - listitem [ref=e844]:
              - group "5 of 10" [ref=e845]:
                - generic [ref=e846]:
                  - generic: Alternative
                - generic [ref=e847]:
                  - generic [ref=e848]:
                    - 'link "September 4, 2026 Various Artists, “Can’t Stop It! II: Australian Post Punk 1979–84” (2026 Deluxe Edition)" [ref=e849] [cursor=pointer]':
                      - /url: https://daily.bandcamp.com/album-of-the-day/various-artists-cant-stop-it-ii-australian-post-punk-1979-84-2026-deluxe-edition-review?from=homepage&ui_context=album_of_the_day
                      - generic [ref=e850]: September 4, 2026
                      - generic [ref=e851]: "Various Artists, “Can’t Stop It! II: Australian Post Punk 1979–84” (2026 Deluxe Edition)"
                    - button "Play" [ref=e854] [cursor=pointer]:
                      - img [ref=e855]
                  - paragraph [ref=e857]: An essential compilation of Australian underground music gets a deluxe vinyl treatment with new bonus tracks.
                  - link "Written by Jude Noel" [ref=e858] [cursor=pointer]:
                    - /url: https://daily.bandcamp.com/contributors/jude-noel
            - listitem [ref=e859]:
              - group "6 of 10" [ref=e860]:
                - generic [ref=e861]:
                  - generic: Hip-Hop/Rap
                - generic [ref=e862]:
                  - generic [ref=e863]:
                    - link "September 3, 2026 Cyst, “ᲘᲘ”" [ref=e864] [cursor=pointer]:
                      - /url: https://daily.bandcamp.com/album-of-the-day/cyst-ee-ee-review?from=homepage&ui_context=album_of_the_day
                      - generic [ref=e865]: September 3, 2026
                      - generic [ref=e866]: Cyst, “ᲘᲘ”
                    - button "Play" [ref=e869] [cursor=pointer]:
                      - img [ref=e870]
                  - paragraph [ref=e872]: The duo of Iglooghost and daisy* develop experimental hip-hop and club music into a timely caricature of everyday life in the UK.
                  - link "Written by Joe Muggs" [ref=e873] [cursor=pointer]:
                    - /url: https://daily.bandcamp.com/contributors/joe-muggs
            - listitem [ref=e874]:
              - group "7 of 10" [ref=e875]:
                - generic [ref=e876]:
                  - generic: Electronic
                - generic [ref=e877]:
                  - generic [ref=e878]:
                    - link "September 2, 2026 RAP, “Navigator”" [ref=e879] [cursor=pointer]:
                      - /url: https://daily.bandcamp.com/album-of-the-day/rap-navigator-review?from=homepage&ui_context=album_of_the_day
                      - generic [ref=e880]: September 2, 2026
                      - generic [ref=e881]: RAP, “Navigator”
                    - button "Play" [ref=e884] [cursor=pointer]:
                      - img [ref=e885]
                  - paragraph [ref=e887]: Another perplexing masterpiece from the duo RAP, surreal and sublime.
                  - link "Written by Sam Davies" [ref=e888] [cursor=pointer]:
                    - /url: https://daily.bandcamp.com/contributors/sam-davies
            - listitem [ref=e889]:
              - group "8 of 10" [ref=e890]:
                - generic [ref=e891]:
                  - generic: Alternative
                - generic [ref=e892]:
                  - generic [ref=e893]:
                    - link "August 31, 2026 Blind Yeo, “The Lemoine Point”" [ref=e894] [cursor=pointer]:
                      - /url: https://daily.bandcamp.com/album-of-the-day/blind-yeo-the-lemoine-point-review?from=homepage&ui_context=album_of_the_day
                      - generic [ref=e895]: August 31, 2026
                      - generic [ref=e896]: Blind Yeo, “The Lemoine Point”
                    - button "Play" [ref=e899] [cursor=pointer]:
                      - img [ref=e900]
                  - paragraph [ref=e902]: The Cornish psych-pop collective keep things moving on their debut, stacking up arrangements and then tearing them down.
                  - link "Written by Hayden Merrick" [ref=e903] [cursor=pointer]:
                    - /url: https://daily.bandcamp.com/contributors/hayden-merrick
            - listitem [ref=e904]:
              - group "9 of 10" [ref=e905]:
                - generic [ref=e906]:
                  - generic: Pop
                - generic [ref=e907]:
                  - generic [ref=e908]:
                    - link "August 28, 2026 Marci, “Mask Lady and Late Night Girl”" [ref=e909] [cursor=pointer]:
                      - /url: https://daily.bandcamp.com/album-of-the-day/marci-mask-lady-and-late-night-girl-review?from=homepage&ui_context=album_of_the_day
                      - generic [ref=e910]: August 28, 2026
                      - generic [ref=e911]: Marci, “Mask Lady and Late Night Girl”
                    - button "Play" [ref=e914] [cursor=pointer]:
                      - img [ref=e915]
                  - paragraph [ref=e917]: The Montreal artist and TOPS member teaches a masterclass in sophisticated, disco-speckled pop.
                  - link "Written by April Clare Welsh" [ref=e918] [cursor=pointer]:
                    - /url: https://daily.bandcamp.com/contributors/april-clare-welsh
            - listitem [ref=e919]:
              - group "10 of 10" [ref=e920]:
                - generic [ref=e921]:
                  - generic: Jazz
                - generic [ref=e922]:
                  - generic [ref=e923]:
                    - link "August 27, 2026 Henry Threadgill, Vijay Iyer & Dafnis Prieto, “Fifteen”" [ref=e924] [cursor=pointer]:
                      - /url: https://daily.bandcamp.com/album-of-the-day/henry-threadgill-vijay-iyer-dafnis-prieto-fifteen-review?from=homepage&ui_context=album_of_the_day
                      - generic [ref=e925]: August 27, 2026
                      - generic [ref=e926]: Henry Threadgill, Vijay Iyer & Dafnis Prieto, “Fifteen”
                    - button "Play" [ref=e929] [cursor=pointer]:
                      - img [ref=e930]
                  - paragraph [ref=e932]: A physically exhilarating listen from three notable figures of modern and experimental jazz.
                  - link "Written by Marshall Gu" [ref=e933] [cursor=pointer]:
                    - /url: https://daily.bandcamp.com/contributors/marshall-gu
      - generic [ref=e934]:
        - generic [ref=e935]:
          - img [ref=e936]
          - img [ref=e938]
        - region "Get the best of Bandcamp Daily" [ref=e940]:
          - generic [ref=e941]:
            - generic [ref=e942]:
              - heading "Get the best of Bandcamp Daily" [level=2] [ref=e944]
              - generic [ref=e946]: Delivered every Friday.
            - generic [ref=e947]:
              - generic [ref=e948]:
                - generic [ref=e949]: Email address
                - textbox "Email address" [ref=e951]
              - button "Sign up" [ref=e952] [cursor=pointer]
    - region "Discover music by genre and location" [ref=e953]:
      - generic [ref=e954]:
        - generic [ref=e955]:
          - heading "Discover music by genre and location" [level=2] [ref=e957]
          - generic [ref=e958]:
            - paragraph [ref=e960]: Dig into genres, sub-genres and scenes from around the world.
            - link "Explore more genres" [ref=e961] [cursor=pointer]:
              - /url: https://bandcamp.com/discover?from=homepage&ui_context=discover_tags
        - generic [ref=e962]:
          - button "prev" [ref=e963] [cursor=pointer]:
            - img [ref=e964]
          - generic [ref=e968]:
            - generic [ref=e969]:
              - link "electronic" [ref=e970] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/electronic?from=homepage&ui_context=discover_tags
              - link "experimental" [ref=e971] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/experimental?from=homepage&ui_context=discover_tags
              - link "alternative" [ref=e972] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/alternative?from=homepage&ui_context=discover_tags
              - link "rock" [ref=e973] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/rock?from=homepage&ui_context=discover_tags
              - link "ambient" [ref=e974] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/ambient?from=homepage&ui_context=discover_tags
              - link "hip-hop/rap" [ref=e975] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/hip-hop-rap?from=homepage&ui_context=discover_tags
              - link "metal" [ref=e976] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/metal?from=homepage&ui_context=discover_tags
              - link "punk" [ref=e977] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/punk?from=homepage&ui_context=discover_tags
              - link "techno" [ref=e978] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/techno?from=homepage&ui_context=discover_tags
              - link "noise" [ref=e979] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/noise?from=homepage&ui_context=discover_tags
              - link "indie" [ref=e980] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/indie?from=homepage&ui_context=discover_tags
              - link "jazz" [ref=e981] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/jazz?from=homepage&ui_context=discover_tags
              - link "instrumental" [ref=e982] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/instrumental?from=homepage&ui_context=discover_tags
              - link "folk" [ref=e983] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/indie-rock?from=homepage&ui_context=discover_tags
              - link "pop" [ref=e984] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/pop?from=homepage&ui_context=discover_tags
              - link "techno" [ref=e985] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/techno?from=homepage&ui_context=discover_tags
              - link "funk" [ref=e986] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/funk?from=homepage&ui_context=discover_tags
              - link "post-rock" [ref=e987] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/post-rock?from=homepage&ui_context=discover_tags
            - generic [ref=e988]:
              - link "house" [ref=e989] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/house?from=homepage&ui_context=discover_tags
              - link "lo-fi" [ref=e990] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/lo-fi?from=homepage&ui_context=discover_tags
              - link "indie pop" [ref=e991] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/indie-pop?from=homepage&ui_context=discover_tags
              - link "shoegaze" [ref=e992] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/shoegaze?from=homepage&ui_context=discover_tags
              - link "synthwave" [ref=e993] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/synthwave?from=homepage&ui_context=discover_tags
              - link "underground hip hop" [ref=e994] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/underground-hip-hop?from=homepage&ui_context=discover_tags
              - link "dream pop" [ref=e995] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/dream-pop?from=homepage&ui_context=discover_tags
              - link "breakcore" [ref=e996] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/breakcore?from=homepage&ui_context=discover_tags
              - link "bedroom pop" [ref=e997] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/bedroom-pop?from=homepage&ui_context=discover_tags
              - link "ambient + field recordings" [ref=e998] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/ambient+field-recordings?from=homepage&ui_context=discover_tags
              - link "beat tape" [ref=e999] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/beat-tape?from=homepage&ui_context=discover_tags
              - link "afrobeats" [ref=e1000] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/afrobeat?from=homepage&ui_context=discover_tags
              - link "future funk" [ref=e1001] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/future-funk?from=homepage&ui_context=discover_tags
              - link "broken beat" [ref=e1002] [cursor=pointer]:
                - /url: https://bandcamp.com/discover/broken-beat?from=homepage&ui_context=discover_tags
            - generic [ref=e1003]:
              - link "Los Angeles" [ref=e1004] [cursor=pointer]:
                - /url: https://bandcamp.com/discover?from=homepage&ui_context=discover_tags&loc=5368361
              - link "Berlin" [ref=e1005] [cursor=pointer]:
                - /url: https://bandcamp.com/discover?from=homepage&ui_context=discover_tags&loc=2950159
              - link "Paris" [ref=e1006] [cursor=pointer]:
                - /url: https://bandcamp.com/discover?from=homepage&ui_context=discover_tags&loc=2988507
              - link "Tokyo" [ref=e1007] [cursor=pointer]:
                - /url: https://bandcamp.com/discover?from=homepage&ui_context=discover_tags&loc=1850144
              - link "San Francisco" [ref=e1008] [cursor=pointer]:
                - /url: https://bandcamp.com/discover?from=homepage&ui_context=discover_tags&loc=5391959
              - link "Detroit" [ref=e1009] [cursor=pointer]:
                - /url: https://bandcamp.com/discover?from=homepage&ui_context=discover_tags&loc=4990729
              - link "São Paulo" [ref=e1010] [cursor=pointer]:
                - /url: https://bandcamp.com/discover?from=homepage&ui_context=discover_tags&loc=3448439
              - link "Hamburg" [ref=e1011] [cursor=pointer]:
                - /url: https://bandcamp.com/discover?from=homepage&ui_context=discover_tags&loc=2911297
              - link "Lisbon" [ref=e1012] [cursor=pointer]:
                - /url: https://bandcamp.com/discover?from=homepage&ui_context=discover_tags&loc=2267056
              - link "Singapore" [ref=e1013] [cursor=pointer]:
                - /url: https://bandcamp.com/discover?from=homepage&ui_context=discover_tags&loc=1880251
              - link "Buenos Aires" [ref=e1014] [cursor=pointer]:
                - /url: https://bandcamp.com/discover?from=homepage&ui_context=discover_tags&loc=3435907
              - link "Barcelona" [ref=e1015] [cursor=pointer]:
                - /url: https://bandcamp.com/discover?from=homepage&ui_context=discover_tags&loc=3128760
              - link "Vietnam" [ref=e1016] [cursor=pointer]:
                - /url: https://bandcamp.com/discover?from=homepage&ui_context=discover_tags&loc=1562822
              - link "Mexico City" [ref=e1017] [cursor=pointer]:
                - /url: https://bandcamp.com/discover?from=homepage&ui_context=discover_tags&loc=3530597
              - link "Lima" [ref=e1018] [cursor=pointer]:
                - /url: https://bandcamp.com/discover?from=homepage&ui_context=discover_tags&loc=3936452
              - link "Egypt" [ref=e1019] [cursor=pointer]:
                - /url: https://bandcamp.com/discover?from=homepage&ui_context=discover_tags&loc=357994
          - button "next" [ref=e1021] [cursor=pointer]:
            - img [ref=e1022]
    - region "Discover merch" [ref=e1024]:
      - generic [ref=e1025]:
        - heading "Discover merch" [level=2] [ref=e1028]
        - list [ref=e1029]:
          - listitem [ref=e1030]:
            - link "Vinyl" [ref=e1031] [cursor=pointer]:
              - /url: https://bandcamp.com/discover/all/vinyl?from=homepage&ui_context=discover_categories
              - generic [ref=e1032]: Vinyl
          - listitem [ref=e1033]:
            - link "CDs" [ref=e1034] [cursor=pointer]:
              - /url: https://bandcamp.com/discover/all/cd?from=homepage&ui_context=discover_categories
              - generic [ref=e1035]: CDs
          - listitem [ref=e1036]:
            - link "Cassettes" [ref=e1037] [cursor=pointer]:
              - /url: https://bandcamp.com/discover/all/cassette?from=homepage&ui_context=discover_categories
              - generic [ref=e1038]: Cassettes
          - listitem [ref=e1039]:
            - link "T-Shirts" [ref=e1040] [cursor=pointer]:
              - /url: https://bandcamp.com/discover/all/tshirt?from=homepage&ui_context=discover_categories
              - generic [ref=e1041]: T-Shirts
    - region "Listening Parties & Live Streams" [ref=e1042]:
      - generic [ref=e1043]:
        - generic [ref=e1044]:
          - generic [ref=e1045]:
            - heading "Listening Parties & Live Streams" [level=2] [ref=e1046]
            - generic [ref=e1047]:
              - button "Prev" [disabled] [ref=e1048] [cursor=pointer]:
                - img [ref=e1049]
              - button "Next" [ref=e1052] [cursor=pointer]:
                - img [ref=e1053]
          - generic [ref=e1056]:
            - paragraph [ref=e1058]: Catch your favorite artist’s Live Stream or join a Listening Party to celebrate their latest release.
            - link "View more events" [ref=e1059] [cursor=pointer]:
              - /url: https://bandcamp.com/live?from=homepage&ui_context=live_carousel
        - status [ref=e1060]
        - list [ref=e1061]:
          - listitem [ref=e1062]:
            - group "1 of 10" [ref=e1063]:
              - generic [ref=e1065]:
                - link "September 13, 2026 at 1:00 PM EDT Hogar Listening Party by El Búho" [ref=e1067] [cursor=pointer]:
                  - /url: https://elbuho.bandcamp.com/merch/hogar-listening-party?from=homepage&ui_context=live_carousel
                  - generic [ref=e1068]: September 13, 2026 at 1:00 PM EDT
                  - generic [ref=e1069]: Hogar Listening Party
                  - generic [ref=e1070]: by El Búho
                - paragraph [ref=e1071]: Join me (El Búho) for the first listen to my new album Hogar, Get a cup of tea, sit in your pyjamas, listen while you have lunch on the couch...feel at home ;) We will also be inviting some of the featured musicians and having an Ask Me Anything in the chat with me (El Búho)
                - generic [ref=e1075]: Free
          - listitem [ref=e1076]:
            - group "2 of 10" [ref=e1077]:
              - generic [ref=e1079]:
                - link "September 13, 2026 at 3:00 PM EDT Harsh Reality Listening Party by The Drowns" [ref=e1081] [cursor=pointer]:
                  - /url: https://thedrowns.bandcamp.com/merch/harsh-reality-listening-party?from=homepage&ui_context=live_carousel
                  - generic [ref=e1082]: September 13, 2026 at 3:00 PM EDT
                  - generic [ref=e1083]: Harsh Reality Listening Party
                  - generic [ref=e1084]: by The Drowns
                - paragraph [ref=e1085]: Join The Drowns for a free listening party 5 days before the album comes out! Noon Seattle time, 3pm EDT, 8pm UK time, 9pm mainland Europe time, etc. The guys will be online to chat about the songs with you!
                - generic [ref=e1089]: Free
          - listitem [ref=e1090]:
            - group "3 of 10" [ref=e1091]:
              - generic [ref=e1093]:
                - link "September 13, 2026 at 3:00 PM EDT here to stay - Listening Party by The Forever Moment" [ref=e1095] [cursor=pointer]:
                  - /url: https://theforevermoment.bandcamp.com/merch/here-to-stay-listening-party?from=homepage&ui_context=live_carousel
                  - generic [ref=e1096]: September 13, 2026 at 3:00 PM EDT
                  - generic [ref=e1097]: here to stay - Listening Party
                  - generic [ref=e1098]: by The Forever Moment
                - paragraph [ref=e1099]: Hi, The Forever Moment is having a listening party to celebrate the 7D Media CD release of "here to stay"! Please join us to for the event! Many thanks, Mark and Steven
                - generic [ref=e1103]: Free
          - listitem [ref=e1104]:
            - group "4 of 10" [ref=e1105]:
              - generic [ref=e1107]:
                - link "September 14, 2026 at 1:00 PM EDT Jenseitsritt Listening Party by Dying Victims Productions" [ref=e1109] [cursor=pointer]:
                  - /url: https://dyingvictimsproductions.bandcamp.com/merch/jenseitsritt-listening-party?from=homepage&ui_context=live_carousel
                  - generic [ref=e1110]: September 14, 2026 at 1:00 PM EDT
                  - generic [ref=e1111]: Jenseitsritt Listening Party
                  - generic [ref=e1112]: by Dying Victims Productions
                - paragraph [ref=e1113]: Join Dying Victims Productions and all 3 Midnight Prey band members for a Q&A sessioin while listening to their new full length albumin its entirety.
                - generic [ref=e1117]: Free
          - listitem [ref=e1118]:
            - group "5 of 10" [ref=e1119]:
              - generic [ref=e1121]:
                - 'link "September 15, 2026 at 11:00 AM EDT FiXT: 20 Years of Noise Listening Party by FiXT" [ref=e1123] [cursor=pointer]':
                  - /url: https://fixtmusic.bandcamp.com/merch/fixt-20-years-of-noise-listening-party?from=homepage&ui_context=live_carousel
                  - generic [ref=e1124]: September 15, 2026 at 11:00 AM EDT
                  - generic [ref=e1125]: "FiXT: 20 Years of Noise Listening Party"
                  - generic [ref=e1126]: by FiXT
                - paragraph [ref=e1127]: "Turn up the volume and join us for the official Bandcamp Listening Party celebrating FiXT: 20 Years of Noise! We’re streaming the entire anniversary compilation from start to finish, bringing together two decades of high-octane electronic-rock, industrial, and metal. Grab your headphones, chat with fellow fans from around the globe, and celebrate twenty years of independent music with us. FiXT President & Co-Founder James Rhodes will be hanging out live in the chat during the stream! Drop in to say hello, ask questions about the label's 20-year history, get behind-the-scenes insights, and hang out with the team."
                - generic [ref=e1131]: Free
          - listitem [ref=e1132]:
            - group "6 of 10" [ref=e1133]:
              - generic [ref=e1135]:
                - link "September 15, 2026 at 3:00 PM EDT ⁺Fragments of Light⁺ Listening Party by Purl" [ref=e1137] [cursor=pointer]:
                  - /url: https://purl.bandcamp.com/merch/fragments-of-light-listening-party?from=homepage&ui_context=live_carousel
                  - generic [ref=e1138]: September 15, 2026 at 3:00 PM EDT
                  - generic [ref=e1139]: ⁺Fragments of Light⁺ Listening Party
                  - generic [ref=e1140]: by Purl
                - paragraph [ref=e1141]: The three of us met once, in Los Angeles 2019, where the seeds were planted that are now flowering. On the 15th of September we will meet again, in the embrace of the colorful waves of sound we have gathered in 'Fragments of Light'. And we'd love to meet you in those waves as well 〜 tune in from wherever you are and whatever state you are in. Hopefully we'll all be soothed, moved and lifted together. We're looking forward to sharing the experience with you! Love from Ludvig (Purl), Emil & Peter (Ecovillage)
                - generic [ref=e1145]: Free
          - listitem [ref=e1146]:
            - group "7 of 10" [ref=e1147]:
              - generic [ref=e1149]:
                - link "September 15, 2026 at 3:30 PM EDT Calm Pieces - Suburbia, Still (Listening Party) by whitelabrecs" [ref=e1151] [cursor=pointer]:
                  - /url: https://whitelabrecs.bandcamp.com/merch/calm-pieces-suburbia-still-listening-party?from=homepage&ui_context=live_carousel
                  - generic [ref=e1152]: September 15, 2026 at 3:30 PM EDT
                  - generic [ref=e1153]: Calm Pieces - Suburbia, Still (Listening Party)
                  - generic [ref=e1154]: by whitelabrecs
                - paragraph [ref=e1155]: Join us for the listening party of 'Suburbia, Still', the second Whitelabrecs album by Calm Pieces! Rafa, the artist, will join us as we listen along in full for the first time. This community event will be a chance to learn more about the album, direct from the artist.
                - generic [ref=e1159]: Free
          - listitem [ref=e1160]:
            - group "8 of 10" [ref=e1161]:
              - generic [ref=e1163]:
                - link "September 16, 2026 at 1:00 PM EDT The London Ambient Orchestra 'Live from Camden' Listening Party by Past Inside the Present" [ref=e1165] [cursor=pointer]:
                  - /url: https://pitp.bandcamp.com/merch/the-london-ambient-orchestra-live-from-camden-listening-party?from=homepage&ui_context=live_carousel
                  - generic [ref=e1166]: September 16, 2026 at 1:00 PM EDT
                  - generic [ref=e1167]: The London Ambient Orchestra 'Live from Camden' Listening Party
                  - generic [ref=e1168]: by Past Inside the Present
                - paragraph [ref=e1169]: We are incredibly honored to welcome The London Ambient Orchestra to the Past Inside the Present family! Please join us for a very special listening party celebrating their debut PITP release, Live from Camden. Come listen with us as we experience the album together in full and celebrate this remarkable new addition to the PITP catalog.
                - generic [ref=e1173]: Free
          - listitem [ref=e1174]:
            - group "9 of 10" [ref=e1175]:
              - generic [ref=e1177]:
                - link "September 16, 2026 at 3:00 PM EDT Two Steps At A Time by Railcard Listening Party by Railcard" [ref=e1179] [cursor=pointer]:
                  - /url: https://railcardband.bandcamp.com/merch/two-steps-at-a-time-by-railcard-listening-party?from=homepage&ui_context=live_carousel
                  - generic [ref=e1180]: September 16, 2026 at 3:00 PM EDT
                  - generic [ref=e1181]: Two Steps At A Time by Railcard Listening Party
                  - generic [ref=e1182]: by Railcard
                - paragraph [ref=e1183]: Come along and join us for a listen through of our new album, ahead of its release on Sept 18th - we'll be here for questions, analysis, explanations etc so be ready to chat if you want to, or feel free to just lurk and listen!! x
                - generic [ref=e1187]: Free
          - listitem [ref=e1188]:
            - group "10 of 10" [ref=e1189]:
              - generic [ref=e1191]:
                - link "September 16, 2026 at 3:00 PM EDT Azizi in Space Listening Party by Sadeedo" [ref=e1193] [cursor=pointer]:
                  - /url: https://sadeedo.bandcamp.com/merch/azizi-in-space-listening-party?from=homepage&ui_context=live_carousel
                  - generic [ref=e1194]: September 16, 2026 at 3:00 PM EDT
                  - generic [ref=e1195]: Azizi in Space Listening Party
                  - generic [ref=e1196]: by Sadeedo
                - paragraph [ref=e1197]: Join Sadeedo (live from Ibiza) for a playback of Azizi In Space and a chat.
                - generic [ref=e1201]: Free
  - region "Player":
    - heading "Player" [level=2] [ref=e1203]
  - contentinfo [ref=e1204]:
    - generic [ref=e1205]:
      - generic [ref=e1206]:
        - heading "Bandcamp Dailyyour guide to the world of Bandcamp" [level=3] [ref=e1207]:
          - link "Bandcamp Daily" [ref=e1208] [cursor=pointer]:
            - /url: https://daily.bandcamp.com/?from=footer&ui_context=editorial_recommendations
          - text: your guide to the world of Bandcamp
        - list [ref=e1209]:
          - listitem [ref=e1210]:
            - link "It’s Not Easy Being Greenland" [ref=e1211] [cursor=pointer]:
              - /url: https://daily.bandcamp.com/scene-report/greenland-music-scene-report?from=footer&ui_context=editorial_recommendations
              - img [ref=e1212]
              - paragraph [ref=e1213]: It’s Not Easy Being Greenland
          - listitem [ref=e1214]:
            - link "Essential Releases, September 11, 2026" [ref=e1215] [cursor=pointer]:
              - /url: https://daily.bandcamp.com/essential-releases/essential-releases-september-11-2026?from=footer&ui_context=editorial_recommendations
              - img [ref=e1216]
              - paragraph [ref=e1217]: Essential Releases, September 11, 2026
          - listitem [ref=e1218]:
            - link "Sylvan Esso Pick Their Bandcamp Favorites" [ref=e1219] [cursor=pointer]:
              - /url: https://daily.bandcamp.com/big-ups/sylvan-esso-bandcamp-favorite-albums?from=footer&ui_context=editorial_recommendations
              - img [ref=e1220]
              - paragraph [ref=e1221]: Sylvan Esso Pick Their Bandcamp Favorites
      - generic [ref=e1222]:
        - heading "On Bandcamp Radio" [level=3] [ref=e1223]
        - generic [ref=e1224]:
          - link "Filmmaker Wes Orshoski joins the show to talk about his new doc on the late Iron Maiden singer." [ref=e1225] [cursor=pointer]:
            - /url: https://bandcamp.com/radio?show=998&play=1&from=footer&ui_context=editorial_recommendations
          - generic [ref=e1226]:
            - link "Filmmaker Wes Orshoski joins the show to talk about his new doc on the late Iron Maiden singer." [ref=e1227] [cursor=pointer]:
              - /url: https://bandcamp.com/radio?show=998&play=1&from=footer&ui_context=editorial_recommendations
              - paragraph [ref=e1228]: Filmmaker Wes Orshoski joins the show to talk about his new doc on the late Iron Maiden singer.
            - link "Listen now" [ref=e1229] [cursor=pointer]:
              - /url: https://bandcamp.com/radio?show=998&play=1&from=footer&ui_context=editorial_recommendations
              - img [ref=e1230]
              - text: Listen now
    - generic [ref=e1232]:
      - navigation [ref=e1233]:
        - generic [ref=e1234]:
          - list [ref=e1235]:
            - listitem [ref=e1236]:
              - link "About" [ref=e1237] [cursor=pointer]:
                - /url: https://bandcamp.com/about?from=footer
            - listitem [ref=e1238]:
              - link "Buttons/Logos" [ref=e1239] [cursor=pointer]:
                - /url: https://bandcamp.com/buttons?from=footer
            - listitem [ref=e1240]:
              - link "Bandcamp Daily" [ref=e1241] [cursor=pointer]:
                - /url: https://daily.bandcamp.com/?from=footer
            - listitem [ref=e1242]:
              - link "Gift Cards" [ref=e1243] [cursor=pointer]:
                - /url: https://bandcamp.com/gift_cards?from=footer
            - listitem [ref=e1244]:
              - link "Bandcamp Merch" [ref=e1245] [cursor=pointer]:
                - /url: https://store.bandcamp.com/?from=footer
            - listitem [ref=e1246]:
              - link "Help" [ref=e1247] [cursor=pointer]:
                - /url: https://get.bandcamp.help/?from=footer
            - listitem [ref=e1248]:
              - link "Jobs" [ref=e1249] [cursor=pointer]:
                - /url: https://bandcamp.com/jobs?from=footer
            - listitem [ref=e1250]:
              - link "Press" [ref=e1251] [cursor=pointer]:
                - /url: https://bandcamp.com/about?from=footer#press
          - generic [ref=e1252]:
            - list [ref=e1253]:
              - listitem [ref=e1254]:
                - link "Bluesky" [ref=e1255] [cursor=pointer]:
                  - /url: https://bsky.app/profile/bandcamp.com
              - listitem [ref=e1256]:
                - link "Facebook" [ref=e1257] [cursor=pointer]:
                  - /url: https://www.facebook.com/Bandcamp
              - listitem [ref=e1258]:
                - link "Instagram" [ref=e1259] [cursor=pointer]:
                  - /url: https://www.instagram.com/bandcamp
              - listitem [ref=e1260]:
                - link "TikTok" [ref=e1261] [cursor=pointer]:
                  - /url: https://www.tiktok.com/@bandcamp
            - list [ref=e1262]:
              - listitem [ref=e1263]:
                - link "Acceptable Use & Moderation Policy" [ref=e1264] [cursor=pointer]:
                  - /url: https://get.bandcamp.help/articles/15263124-bandcamp-s-acceptable-use-and-moderation-policy?from=footer
              - listitem [ref=e1265]:
                - link "Fair Trade Music Policy" [ref=e1266] [cursor=pointer]:
                  - /url: https://bandcamp.com/fair_trade_music_policy?from=footer
              - listitem [ref=e1267]:
                - link "Copyright" [ref=e1268] [cursor=pointer]:
                  - /url: https://bandcamp.com/copyright?from=footer
              - listitem [ref=e1269]:
                - link "Privacy" [ref=e1270] [cursor=pointer]:
                  - /url: https://bandcamp.com/privacy?from=footer
              - listitem [ref=e1271]:
                - link "Terms of Use" [ref=e1272] [cursor=pointer]:
                  - /url: https://bandcamp.com/terms_of_use?from=footer
              - listitem [ref=e1273]:
                - button "Cookie Settings" [ref=e1274] [cursor=pointer]
        - generic [ref=e1275]:
          - list [ref=e1276]:
            - listitem [ref=e1277]:
              - link "Bandcamp for Artists" [ref=e1278] [cursor=pointer]:
                - /url: https://bandcamp.com/artists?from=footer
            - listitem [ref=e1279]:
              - link "Bandcamp for Fans" [ref=e1280] [cursor=pointer]:
                - /url: https://bandcamp.com/fans?from=footer
            - listitem [ref=e1281]:
              - link "Bandcamp for Labels" [ref=e1282] [cursor=pointer]:
                - /url: https://bandcamp.com/labels?from=footer
          - generic [ref=e1283]:
            - paragraph [ref=e1284]: "Apps:"
            - list [ref=e1285]:
              - listitem [ref=e1286]:
                - link "Android" [ref=e1287] [cursor=pointer]:
                  - /url: https://play.google.com/store/apps/details?id=com.bandcamp.android
              - listitem [ref=e1288]:
                - link "iOS" [ref=e1289] [cursor=pointer]:
                  - /url: https://itunes.apple.com/us/app/bandcamp/id706408639?mt=8
          - 'button "Language: English" [ref=e1291] [cursor=pointer]'
      - link "Bandcamp home" [ref=e1292] [cursor=pointer]:
        - /url: https://bandcamp.com/?from=footer&ui_context=logo
        - img [ref=e1293]
        - generic [ref=e1296]: Bandcamp home
```

# Test source

```ts
  142 |                 type: 'jpeg',
  143 |             });
  144 |         } catch (e: any) {
  145 |             console.error(`Failed to take screenshot ${name}`, e.message);
  146 |         }
  147 |     }
  148 | 
  149 |     async messageCallback({ frame }: { frame: Frame }, msg: ContentScriptMessage) {
  150 |         LOG_MESSAGES.includes(msg.type) && console.log(msg);
  151 |         this.received.push(msg);
  152 |         switch (msg.type) {
  153 |             case 'init': {
  154 |                 const url = frame.url();
  155 |                 const mainFrame = frame.parentFrame() === null;
  156 |                 // Use full rules for optIn (compact rules omit optIn steps), compact rules for optOut.
  157 |                 const rules =
  158 |                     this.autoAction === 'optIn'
  159 |                         ? { autoconsent: fullRules }
  160 |                         : { compact: filterCompactRules(compactRules, { url, mainFrame }) };
  161 |                 await frame.evaluate(
  162 |                     `autoconsentReceiveMessage({ type: "initResp", config: ${JSON.stringify({
  163 |                         enabled: true,
  164 |                         autoAction: this.autoAction,
  165 |                         disabledCmps: [],
  166 |                         enablePrehide: false,
  167 |                         detectRetries: 20,
  168 |                         enableCosmeticRules: true,
  169 |                         visualTest: true,
  170 |                     })}, rules: ${JSON.stringify(rules)} })`,
  171 |                 );
  172 |                 break;
  173 |             }
  174 |             case 'cmpDetected': {
  175 |                 await this.takeScreenshot(`${this.screenshotCounter++}-cmpDetected`);
  176 |                 break;
  177 |             }
  178 |             case 'popupFound': {
  179 |                 await this.takeScreenshot(`${this.screenshotCounter++}-popupFound`);
  180 |                 break;
  181 |             }
  182 |             case 'optInResult':
  183 |             case 'optOutResult': {
  184 |                 await this.takeScreenshot(`${this.screenshotCounter++}-result`);
  185 |                 if (msg.scheduleSelfTest) {
  186 |                     this.selfTestFrame = frame;
  187 |                 }
  188 |                 break;
  189 |             }
  190 |             case 'autoconsentDone': {
  191 |                 await this.takeScreenshot(`${this.screenshotCounter++}-done`);
  192 |                 if (this.selfTestFrame && this.options.testSelfTest) {
  193 |                     await this.selfTestFrame.evaluate(`autoconsentReceiveMessage({ type: "selfTest" })`);
  194 |                 }
  195 |                 break;
  196 |             }
  197 |             case 'eval': {
  198 |                 const result = await frame.evaluate(msg.code);
  199 |                 await frame.evaluate(`autoconsentReceiveMessage({ id: "${msg.id}", type: "evalResp", result: ${JSON.stringify(result)} })`);
  200 |                 break;
  201 |             }
  202 |             case 'visualDelay': {
  203 |                 await this.takeScreenshot(`${this.screenshotCounter++}`);
  204 |                 break;
  205 |             }
  206 |             case 'autoconsentError': {
  207 |                 console.error(this.url, msg.details);
  208 |                 break;
  209 |             }
  210 |         }
  211 |     }
  212 | 
  213 |     // inject content scripts into every frame
  214 |     async injectContentScripts() {
  215 |         await this.injectContentScript(this.page);
  216 |         this.page.frames().forEach((frame) => this.injectContentScript(frame));
  217 |         this.page.on('framenavigated', (frame) => this.injectContentScript(frame));
  218 |     }
  219 | 
  220 |     findReceivedMessages(msg: Partial<ContentScriptMessage>) {
  221 |         return this.received.filter((m) => {
  222 |             return Object.keys(msg).every((k) => (<any>m)[k] === (<any>msg)[k]);
  223 |         });
  224 |     }
  225 | 
  226 |     isMessageReceived(msg: Partial<ContentScriptMessage>) {
  227 |         return this.findReceivedMessages(msg).length > 0;
  228 |     }
  229 | 
  230 |     waitForMessage(msg: Partial<ContentScriptMessage>, maxTimes = 50, interval = 500) {
  231 |         return waitFor(() => this.isMessageReceived(msg), maxTimes, interval);
  232 |     }
  233 | 
  234 |     async assertMessageReceived(
  235 |         failureMessage: string,
  236 |         msg: Partial<ContentScriptMessage>,
  237 |         expectedState = true,
  238 |         maxTimes = 50,
  239 |         interval = 500,
  240 |     ) {
  241 |         await this.waitForMessage(msg, maxTimes, interval);
> 242 |         expect(this.isMessageReceived(msg), failureMessage).toBe(expectedState);
      |                                                             ^ Error: selfTestResult received, but failed
  243 |     }
  244 | 
  245 |     async assertNoReloadLoop() {
  246 |         try {
  247 |             await this.page.waitForLoadState('networkidle', { timeout: 5000 });
  248 |         } catch (e) {
  249 |             // ignore timeout errors
  250 |         }
  251 |         await this.page.waitForTimeout(3000); // capture potential reloads
  252 |         // check that popupFound messages are unique
  253 |         const popupFoundMessages = this.findReceivedMessages({ type: 'popupFound' });
  254 |         for (let i = 0; i < popupFoundMessages.length; i++) {
  255 |             for (let j = i + 1; j < popupFoundMessages.length; j++) {
  256 |                 expect(popupFoundMessages[i], `Possible reload loop: found multiple identical popupFound messages`).not.toEqual(
  257 |                     popupFoundMessages[j],
  258 |                 );
  259 |             }
  260 |         }
  261 | 
  262 |         if (this.options.expectPopupOpen) {
  263 |             // check that the autoconsentDone message was received the expected number of times (typically 1)
  264 |             expect(
  265 |                 this.findReceivedMessages({ type: 'autoconsentDone' }).length,
  266 |                 'Possible reload loop: too many autoconsentDone messages',
  267 |             ).toBeLessThanOrEqual(this.options.expectedRuns);
  268 |         }
  269 |     }
  270 | 
  271 |     async runAssertions() {
  272 |         await this.assertMessageReceived(`no CMP detected`, { type: 'cmpDetected' });
  273 | 
  274 |         const expectedCmpDetected: Partial<ContentScriptMessage> = { type: 'cmpDetected', cmp: this.expectedCmp };
  275 |         await this.assertMessageReceived(`detected a wrong CMP`, expectedCmpDetected);
  276 | 
  277 |         const expectedPopupFound: Partial<ContentScriptMessage> = { type: 'popupFound', cmp: this.expectedCmp };
  278 |         await this.assertMessageReceived(
  279 |             `expected popup not found`,
  280 |             expectedPopupFound,
  281 |             this.options.expectPopupOpen,
  282 |             this.options.expectPopupOpen ? 50 : 5,
  283 |             500,
  284 |         );
  285 | 
  286 |         await this.assertNoReloadLoop();
  287 | 
  288 |         if (this.options.expectPopupOpen) {
  289 |             // first long wait for autoconsentDone
  290 |             await this.assertMessageReceived(`autoconsentDone not received`, { type: 'autoconsentDone' }, true, 90, 500);
  291 |             await this.assertMessageReceived(
  292 |                 `autoconsentDone received for unexpected CMP`,
  293 |                 { type: 'autoconsentDone', cmp: this.expectedCmp },
  294 |                 true,
  295 |                 90,
  296 |                 500,
  297 |             );
  298 | 
  299 |             await this.assertNoReloadLoop();
  300 | 
  301 |             // short waits for other messages because they should have already arrived by now
  302 |             if (this.autoAction === 'optOut') {
  303 |                 await this.assertMessageReceived(`optOutResult not received`, { type: 'optOutResult' }, true, 1, 300);
  304 |                 await this.assertMessageReceived(`optOutResult received, but failed`, { type: 'optOutResult', result: true }, true, 1, 300);
  305 |             }
  306 |             if (this.autoAction === 'optIn') {
  307 |                 await this.assertMessageReceived(`optInResult not received`, { type: 'optInResult' }, true, 1, 300);
  308 |                 await this.assertMessageReceived(`optInResult received, but failed`, { type: 'optInResult', result: true }, true, 1, 300);
  309 |             }
  310 |             if (this.options.testSelfTest && this.selfTestFrame) {
  311 |                 await this.assertMessageReceived(`selfTestResult not received`, { type: 'selfTestResult' }, true, 1, 300);
  312 |                 await this.assertMessageReceived(
  313 |                     `selfTestResult received, but failed`,
  314 |                     { type: 'selfTestResult', result: true },
  315 |                     true,
  316 |                     1,
  317 |                     300,
  318 |                 );
  319 |             }
  320 |         }
  321 | 
  322 |         this.received.forEach((msg) => {
  323 |             if (msg.type === 'autoconsentError') {
  324 |                 expect(msg.details.msg, 'only "multiple CMPs" errors are allowed').toContain('Found multiple CMPs');
  325 |             }
  326 |         });
  327 |     }
  328 | }
  329 | 
  330 | export default function generateCMPTests(cmp: string, sites: string[], overrideOptions: Partial<TestOptions> = {}) {
  331 |     test.describe(cmp, () => {
  332 |         sites.forEach((url) => {
  333 |             const finalOptions = { ...defaultOptions, ...overrideOptions };
  334 |             if (finalOptions.onlyRegions && finalOptions.onlyRegions.length > 0 && !finalOptions.onlyRegions.includes(testRegion)) {
  335 |                 return;
  336 |             }
  337 |             if (finalOptions.skipRegions?.includes(testRegion)) {
  338 |                 return;
  339 |             }
  340 | 
  341 |             const domain = new URL(url).hostname;
  342 |             const urlHash = crypto.createHash('md5').update(url).digest('hex').slice(0, 4);
```