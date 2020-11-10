/* eslint-disable  */
$(document).ready(() => {
	const center = ol.proj.fromLonLat([longitude, latitude]);
	const pinnedLocation = ol.proj.transform(center, 'EPSG:3857', 'EPSG:4326');
	const feature = new ol.Feature(new ol.geom.Point(center));
	var map = new ol.Map({
		target: 'map',
		layers: [
			new ol.layer.Tile({
				source: new ol.source.OSM()
			}),
			new ol.layer.Vector({
				source: new ol.source.Vector({
					features: [feature]
				}),
				style: new ol.style.Style({
					image: new ol.style.Icon({
						src: pinIconSrc
					})
				})
			})
		],
		view: new ol.View({
			center: center,
			zoom: 15
		})
	});
})
