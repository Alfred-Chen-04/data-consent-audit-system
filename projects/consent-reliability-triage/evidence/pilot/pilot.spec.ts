import generateCMPTests from '../playwright/runner';
generateCMPTests('bandcamp.com', ['https://bandcamp.com/'], { testOptIn: false });
