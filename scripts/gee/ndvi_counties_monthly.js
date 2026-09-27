// GEE script: NDVI monthly extraction for Kenya's 47 counties (2017-2024)
// Run in: https://code.earthengine.google.com
// Asset required: projects/kenya-maize-monitor/assets/kenya_counties_shp
// Output: ndvi_counties_monthly_2017_2024.csv (Google Drive)

var counties = ee.FeatureCollection(
  'projects/kenya-maize-monitor/assets/kenya_counties_shp'
);

function maskS2Clouds(image) {
  var qa = image.select('QA60');
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
      .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
  return image.updateMask(mask).divide(10000);
}

var years = ee.List.sequence(2017, 2024);
var months = ee.List.sequence(1, 12);

var features = years.map(function(y) {
  var year = ee.Number(y);
  return months.map(function(m) {
    var month = ee.Number(m);
    var start = ee.Date.fromYMD(year, month, 1);
    var end = start.advance(1, 'month');

    var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
        .filterDate(start, end)
        .filterBounds(counties)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 40))
        .map(maskS2Clouds);

    var ndvi = s2.map(function(img) {
      return img.normalizedDifference(['B8', 'B4']).rename('NDVI');
    }).mean();

    var stats = ndvi.reduceRegions({
      collection: counties,
      reducer: ee.Reducer.mean(),
      scale: 1000,
    });

    return stats.map(function(f) {
      return f.set({
        year: year,
        month: month,
        date: start.format('YYYY-MM-dd')
      });
    });
  });
}).flatten();

var all = ee.FeatureCollection(features).flatten();

Export.table.toDrive({
  collection: all,
  description: 'ndvi_kenya_counties_2017_2024',
  folder: 'kenya_climate_data_lab',
  fileNamePrefix: 'ndvi_counties_monthly_2017_2024',
  fileFormat: 'CSV',
  selectors: ['name', 'year', 'month', 'date', 'mean']
});
