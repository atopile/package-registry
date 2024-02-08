const million = require('million/compiler');
module.exports = {
  plugins: [
    million.webpack({ auto: true }),
  ],
};
