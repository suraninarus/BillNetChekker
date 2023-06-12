use Dijnet;

drop table szamlak;
commit;
create table if not exists szamlak(
id int primary key auto_increment ,
Szamlakibocsato varchar(32),
Tranzakcio_azonosito varchar(32),
Szamla_kelte date,
Befizetes_datuma date,
Osszeg int,
Ugyfelazonosito int,
Szamlaszam varchar(32),
SimplePay_tranzakcioazonosito varchar(32) default null,
Eredeti_Szamla_lementve boolean
)
;

insert into szamlak(
                Szamlakibocsato,
                Tranzakcio_azonosito,
                Szamla_kelte,
                Befizetes_datuma,
                Osszeg,
                Ugyfelazonosito,
                Szamlaszam,
                SimplePay_tranzakcioazonosito,
                Eredeti_Szamla_lementve
) values (
                "FŐTÁV Zrt.",
                129399076,
                "2020-12-14",
                "2020-12-18",
                19276,
                30007506,
                3310702882,
                "igen",
                null
)
;
commit;

select * from szamlak;
use Dijnet;

select * from szamlak;
use Dijnet;

insert into szamlak values (
                3,
        "FŐTÁV Zrt.",
                129399076,
                "2020-12-14",
                "2020-12-18",
                19276,
                30007506,
                3310702882,
                null,
                true
)
;


