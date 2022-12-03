
create table if not exists station(
station_id int primary key,
	station_name varchar,
	station_owner varchar,
	longitude float,
	latitude float,
	height float
);

create table if not exists temperature (
	station_id int references station(station_id),
	temperature_id serial primary key,
	value float,
	timestamp varchar(30),
	quality char(1)
);

SELECT s.station_name, t.value from station s join
temperature t on t.station_id = s.station_id;
--SELECT * FROM station;