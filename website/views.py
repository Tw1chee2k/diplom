from flask import Blueprint, render_template, request, flash, redirect, url_for, json
from flask_login import login_required, current_user, logout_user
from .models import Comment, Tovar, Cart, Order, Sklad, User, Point, Message
from . import db
from werkzeug.security import generate_password_hash
import googlemaps
from collections import defaultdict
from sqlalchemy import func
from datetime import datetime
import os
from flask_admin import expose, AdminIndexView

views = Blueprint('views', __name__)
current_date = datetime.now().date()

def get_items_cart():
    total_quantity = db.session.query(func.sum(Cart.quantity)).filter_by(user_email=current_user.email).scalar()
    return total_quantity

@views.route('/')
def catalog():
    if User.query.count() == 0:
        user_data = [
                ('Admin', 'Tw1', 'tw1che.2k@gmail.com', '1234'),
                ( None, 'Gold','gold.10.boy@gmail.com', '1234'),
            ]
        for data in user_data:
            user = User(
                type = data[0],
                nickname = data[1],
                email = data[2],
                password = generate_password_hash(data[3])
            )
            db.session.add(user)
        
    if Sklad.query.count() == 0:
        sklad_data = [
            'Nalibokskaya 14',
        ]
        for street in sklad_data:
            sklad = Sklad(
                street=street
            )
            db.session.add(sklad)
        db.session.commit()
 
    if Tovar.query.count() == 0:
        Tovar_data = [
            ('Tokyo Ghoul', 'Mat', 0, 29.99, 'Soon', 'Anime', '450x400mm', '4mm', 'Cloth', 'Eco-friendly Rubber', 'This gaming mat is suitable for all ELO abusers with FACEIT, especially the bold pixel art will be appreciated by fans of bright and colorful devices! The soft coating provides maximum comfort with any mouse sensitivity used. The rubber base guarantees the mat immobility during sudden movements.', 1, 'Tokyo_Ghoul'), 
			('Samurai red', 'Mat', 65, 29.99, 'In stoke', 'Pixel art', '450x400mm', '4mm', 'Cloth', 'Eco-friendly Rubber', 'A samurai has no purpose, only a path... This mat will fit perfectly and decorate the setup! Colorful art is suitable for absolutely everyone, from novice game lovers to top esports players from different parts of the gaming world!', 1, 'Samurai_red'),
			('Samurai Large', 'Mat', 24, 39.99, 'In stoke', 'Pixel art', '900x400mm', '4mm', 'Cloth', 'Eco-friendly Rubber', 'A samurai has no purpose, only a path... This mat will fit perfectly and decorate the setup! Colorful art is suitable for absolutely everyone, from novice game lovers to top esports players from different parts of the gaming world!', 1, 'Samurai_Large'),      
			('Pixel Art Mirage', 'Mat', 44, 29.99, 'In stoke', 'Pixel art', '450x400mm', '4mm', 'Cloth', 'Eco-friendly Rubber', 'This gaming mat is suitable for all ELO abusers with FACEIT, especially the bold pixel art will be appreciated by fans of bright and colorful devices! The soft coating provides maximum comfort with any mouse sensitivity used. The rubber base guarantees the mat immobility during sudden movements.', 1, 'Pixel_Art_Mirage'),
			('Pixel Art Inferno', 'Mat', 52, 29.99, 'In stoke', 'Pixel art', '450x400mm', '4mm', 'Cloth', 'Eco-friendly Rubber', 'This gaming mat is suitable for all ELO abusers with FACEIT, especially the bold pixel art will be appreciated by fans of bright and colorful devices! The soft coating provides maximum comfort with any mouse sensitivity used. The rubber base guarantees the mat immobility during sudden movements.', 1, 'Pixel_Art_Inferno'),  
			('Samurai', 'Mat', 24, 29.99, 'In stoke', 'Pixel art', '450x400mm', '4mm', 'Cloth', 'Eco-friendly Rubber', 'A samurai has no purpose, only a path... This mat will fit perfectly and decorate the setup! Colorful art is suitable for absolutely everyone, from novice game lovers to top esports players from different parts of the gaming world!', 1, 'Samurai'),
			('Pixel Art Dust II', 'Mat',  14, 29.99, 'In stoke', 'Pixel art', '450x400mm', '4mm', 'Cloth', 'Eco-friendly Rubber', 'This gaming mat is suitable for all ELO abusers with FACEIT, especially the bold pixel art will be appreciated by fans of bright and colorful devices! The soft coating provides maximum comfort with any mouse sensitivity used. The rubber base guarantees the mat immobility during sudden movements.', 1, 'Pixel_Art_Dust_II'),    
			('Black A1', 'Mat', 4, 29.99, 'In stoke', 'Black', '450x400mm', '4mm', 'Cloth', 'Eco-friendly Rubber', 'This gaming mat is suitable for all ELO abusers with FACEIT, especially the bold pixel art will be appreciated by fans of bright and colorful devices! The soft coating provides maximum comfort with any mouse sensitivity used. The rubber base guarantees the mat immobility during sudden movements.', 1, 'Black_A1'),    
            ('Mixed Angularity', 'Mat',  0, 29.99, 'Sold', 'Black', '450x400mm', '4mm', 'Cloth', 'Eco-friendly Rubber', 'This gaming mat is suitable for all ELO abusers with FACEIT, especially the bold pixel art will be appreciated by fans of bright and colorful devices! The soft coating provides maximum comfort with any mouse sensitivity used. The rubber base guarantees the mat immobility during sudden movements.', 1, 'Mixed_Angularity'),    
        ]
        for data in Tovar_data:
            tovar = Tovar(
                name=data[0],
                type = data[1],
		        count=data[2],
		        cost = data[3],
                status = data[4],
                color = data[5],
                size = data[6],
                thickness = data[7],
                material = data[8],
                base = data[9],
                info = data[10],
                sklad_id = data[11], 
                img_name = data[12]
            )
            db.session.add(tovar)
        
    if Point.query.count() == 0:
        point_data = [
        ('Minsk', 'ul. Installers, 2 Euroopt', 1),
        ('Minsk', 'ul. Prytytsky , 29 1st floor of the Tikali shopping center', 6),
        ('Minsk', 'ul. Kazimirovskaya, 6 m-n Euroopt', 9),
        ('Gomel', 'ul. Kirova, 136 m-n Euroopt', 10),
        ('Vitebsk', 'ave. Builders, 15-2 m-n "Euroopt"', 11),
        ('Lida', 'ul. Krasnoarmeyskaya, 63 m-n Euroopt', 23),
        ('Bobruisk', 'ul. Minskaya, 111 m-n "Euroopt"', 27),
        ('Smorgon', 'ul. Kolasa, 120a m-n "Euroopt"', 29),
        ('Osipovichi', 'ul. Leninskaya, 86B m-n "Kopeechka"', 33),
        ('Glubokoe', 'ul. Lenin, 9A-1 m-n "Euroopt"', 35),
        ('Grodno', 'ul. Solomova, 104/1 m-n "Euroopt"', 37),
        ('Lida', 'ul. Gagarina, 27 m-n "Euroopt"', 38),
        ('Slonim', 'Yershova str., 58 m-n "Euroopt"', 41),
        ('Minsk', 'ul. Bogdanovich, 134 m-n "Hit"', 50),
        ('Svisloch', 'ul. Tsagelnik, 12 m-n "Euroopt"', 51),
        ('Mstislavl', 'Peter Mstislavets str., 1 m-n Euroopt', 53),
        ('Zhlobin', 'mkr. 18th, 43 m-n "Kopek"', 54),
        ('Novogrudok', 'ul. Sovetskaya, 17 m-n "Euroopt"', 57),
        ('Zhodino', 'Gagarin str., 20A', 59),
        ('Dzerzhinsk', 'Minskaya str., 27', 60),
        ('Rogachev', 'Bogatyreva str., 118 m-n "Euroopt"', 61),
        ('Mogilev', '79 Gagarin str., m-n "Euroopt"', 62),
        ('Grodno', ' ave. Kupala, 82A m-n "Euroopt"', 63),
        ('Vitebsk', 'ave. Moskovsky, 130 m-n "Euroopt"', 64),
        ('Brest', 'Varshavskoe highway, 11 m-n "Euroopt"', 65),
        ('Minsk', ' ave. Pushkin, 29b m-n "Groshyk"', 69),
        ('Minsk', ' ave. Pobediteley, 89 m-n "Euroopt"', 74),
        ('Soligorsk', 'Zheleznodorozhnaya str., 12a m-n "Euroopt"', 77),
        ('Ivatsevichi', 'ul. Sovetskaya, 1A', 80),
        ('Narovlya', 'Korzun A.G. str., 64', 83),
        ('Branch', 'Zaslonov str.', 84),
        ('Chechersk', ' lane Pervomaisky, 4', 85),
        ('Bridges', ' ave. Mira, 2a', 88),
        ('Gomel', ' Khataevich str., 9', 89),
        ('Minsk', 'Umanskaya str., 54 Globo shopping center near the parking lot', 92),
        ('Baranovichi', 'ul. Textile, 14a m-n "Euroopt"', 93),
        ('Klichev', 'Zaytsa str., 4a m-n "Euroopt"', 94),
        ('Minsk', 'ave. Rokossovsky, 99', 96),
        ('Minsk', 'Yesenin str., 76', 100),
        ('Minsk', 'Masherov Ave., 51', 107),
        ('Minsk', 'ul. Kazinets, 52a', 108),
        ('Mogilev',  '40A Movchanskogo str.', 112),
        ('Petrikov', '3B Paper street', 115),
        ('Shumilino', 'Leninskaya Street, 32 m-n "Euroopt"', 119),
        ('Vitebsk', ' ave. Moskovsky, 60a', 121),
        ('Minsk', ' 44 Yankovsky str.', 123),
        ('Minsk', ' Alibegova str., 13/1', 125),
        ('Brest', ' ul. 17 September, 49', 126),
        ('Vitebsk', ' Lenin str., 26a', 127),
        ('Brest', 'Raduzhnaya str., 150', 128),
        ('Lelchitsy', ' ul. Sovetskaya, 28', 130),
        ('Vileika', 'Chapaev str., 60', 131),
        ('Mozyr', 'ul. Studentskaya, 46', 132),
        ('Brest', 'St. Orlovskaya, 50', 136),
        ('Minsk', 'Matusevich str., 35G', 137),
        ('Khoiniki', '70 let Oktyabrya str., 1', 138),
        ('Chashniki', 'ul. Cosmonauts, 4', 139),
        ('Khotimsk', 'ul. Leninskaya, 1', 140),
        ('Braslav', 'Dzerzhinsky str., 28B', 141),
        ('Minsk', 'Goshkevich str., 3', 142),
        ('Molodechno', 'ul. Budavnikov, 17A', 146),
        ('Glusk', 'ul. Gagarina, 25', 147),
        ('Minsk', 'ul. Shpilevsky, 54', 148),
        ('Grodno', 'ul. Oginsky, 12', 151),
        ('Brest', 'Moskovskaya str., 342', 152),
        ('Minsk', 'ya.Kolas str., 53/1', 158),
        ('Minsk', 'Lyubimova Ave., 26', 159),
        ('Minsk', 'Aerodromnaya str., 28', 160),
        ('Minsk', 'ul. Vodolazhsky, 15', 161),
        ('Minsk', 'Burdeynogo str., 6B (shopping center "TOP")', 165),
        ('Minsk', 'ul. Karvata, 31a', 167),
        ('Baranovichi', 'ul. Communist, 5', 168),
        ('Mogilev', 'ul. Chestnut, 4', 175),
        ('Mozyr', 'b-R. Friendship, 3a', 176),
        ('Novopolotsk', 'ul. Yeronko, 7a', 178),
        ('Rechitsa', 'ul. Dostoevsky, 27-54', 180),
        ('Minsk', 'ul. Prushinsky, 2', 182),
        ('Minsk', 'ul. Bagration, 55b', 183),
        ('Pinsk', 'ul. Brest, 72a', 186),
        ('Kopyl', 'ul. Partizanskaya, 1a', 187),
        ('Gomel', 'ave. Rechitsky, 5B', 190),
        ('Gorki', 'ul. Sovetskaya, 9', 192),
        ('Gomel', 'ul. Kirova, 25', 193),
        ('Minsk', 'ave. Partizansky, 13', 194),
        ('Gantsevichi', 'ul. Builders, 11B', 200),
        ('Gomel', 'ul. Tsarikova, 1/2', 203),
        ('Minsk', 'ave. Dzerzhinsky, 23-431', 206),
        ('Vitebsk', 'ave. Frunze, 37', 208),
        ('Minsk', 'tr-T. Smorgovsky, 7-93', 211),
        ('Ivanovo', 'ul. Sovetskaya, 55', 216),
        ('Kamenets', 'ul. Borderline, 22', 217),
        ('Verkhnedvinsk', 'ul. Leninskaya, 15b-1', 218),
        ('Baranovichi', 'ave. Sovetsky, 35', 219), 
        ('Gomel', '62A Rechitsky Ave.', 220),
        ('Orsha', 'ul. Mira, 49', 221),
        ('Buda-Koshelevo', 'ul. Lenin, 58', 223),
        ('Round', 'street Moprovskaya, 6 (m-n "Euroopt")', 224),
        ('Minsk', 'ul. Jerzy Gedroica, 2', 226),
        ('Zhitkovichi', 'ul. Chkalova, 6', 228),
        ('Ivye', 'Karl Marx Street, 19', 232),
        ('Berezino', 'ul. Honinova, 29b1', 236),
        ('Soligorsk', 'ul. Embankment, 25A', 239),
        ('Cherven', 'ul. Leninskaya, 5', 242),
        ('Minsk', 'ul. Lobanka, 22', 244),
        ('Kolodishchi', 'ul. Minsk, 69A', 246),
        ('Yelsk', 'Dzerzhinskiy str., 20-2', 249),
        ('Bykhov', 'ul. Bogdan Khmelnitsky, 1', 250),
        ('Slutsk', 'ul.Socialist, 144a', 251),
        ('Druzhny', 'ul.Chepika, 26', 253),
        ('Fanipol', 'ul. Chapsky, 15', 256),
        ('Miory', 'str. Sadovaya, 1', 260),
        ('Drogichin', 'ul. Reclamation, 43/1', 262),
        ('Berezovka', 'ul. Komsomolskaya 22', 263),
        ('Grodno', 'ul. Soviet Border Guards, 91', 264),
        ('Grodno', 'str. Dovator, 7', 265),
        ('Orsha', 'Alexey Garanin Ave., 4', 267),
        ('Minsk', 'ul.Mogilevskaya, 14', 269),
        ('Borisov', 'ul. Normandy-Neman, 145', 276),
        ('Bobruisk', 'ul. Sovetskaya, 113', 279),
        ('Mogilev', 'ul. Pervomaiskaya, 69A', 282),
        ('Lyuban', 'ul. Sovetskaya, 31', 284),
        ('Minsk', 'ave. Dzerzhinsky, 104k2, room117, entrance through the business center', 285),
        ('Beloozersk', 'ul. Lenin, 50A', 286),
        ('Logoisk', 'Gainenskoe highway, 1-117', 287),
        ('Luninets', 'ul. Sovetskaya, 13-3', 289),
        ('Grodno', 'Kurchatov str., 47', 292),
        ('Minsk', 'ul.Lozhinskaya, 20', 294),
        ('Kalinkovichi', 'ul. 50 let Oktyabrya, 83', 295),
        ('Oshmyany', 'ul. Pionerskaya, 2', 299),
        ('Minsk', 'ul.Tashkent, 10', 300),
        ('Brest', 'St.Rokossovsky, 3-85', 302),
        ('Minsk', 'ave. Dzerzhinsky, 11', 303),
        ('Novopolotsk', 'Molodezhnaya str., 51-63', 305),
        ('Minsk', 'ul.Kamennogorskaya, 6-203', 311),
        ('Mogilev', 'ul. Arkady Kuleshova, 1', 312),
        ('Minsk', 'ul. Kulman, 5B-72, Pavilion No.135', 314),
        ('Mogilev', 'ave. Pushkinskiy, 30 (m-n "Euroopt")', 318),
        ('Skidel', 'ul. Gagarina, 11', 319),
        ('Lida', 'ul. Sovetskaya, 41-3', 320),
        ('Bobruisk', 'ul. Batova, 19-A', 322),
        ('Slutsk', 'Levonyan str., 31A', 324),
        ('Cherikov', 'ul. Leninskaya Street, 178', 325),
        ('Zhabinka', 'ul. Naganova, 16a/2', 326),
        ('Minsk', 'ul. Akademika Zhebraka, 35', 327),
        ('Smolevichi', '50 let Oktyabrya str., 4-2', 328),
        ('Mogilev', 'ul. Lazarenko, 73a', 329),
        ('Minsk', 'Surganova str., 57b-8', 331),
        ('Brest', 'St. Komsomolskaya, 8-1 (m-n "Euroopt")', 333),
        ('Brest', 'Lutskaya str., 48', 334),
        ('Pinsk', 'ul. Karaseva, 6', 335),
        ('Kobrin', 'Dzerzhinskiy str., 115b', 336),
        ('Grodno', 'ul. Antonova, 14-43', 337),
        ('Luninets', 'ul. Krasnaya, 107-2', 339),
        ('Ostrovets', 'Karl Marx Street, 1', 340),
        ('Polotsk', 'ul. Petrusya Brovki, 45-2', 341),
        ('Vitebsk', 'ul. Chkalova, 56-154', 342),
        ('Nesvizh', 'ul. Leninskaya, 115', 343),
        ('Vitebsk', '3rd Zmitroka Byaduli str., 28-2', 346),
        ('Brest', 'ave. Masherova, 59-41', 347),
        ('Polotsk', 'Pushkin str., 20-1', 351),
        ('Kalinkovichi', 'ul.Sovetskaya, 96-1', 352),
        ('Minsk', 'ul. Angarsk, 62a', 354),
        ('Dyatlovo', 'ul. Gorky, 12', 357),
        ('Lepel', 'Chuikov str., 75', 358),
        ('Chausy', 'Azarov str., 2A', 359),
        ('Slutsk', 'ul. Lenin, 187-1', 361),
        ('Minsk', ' Belinsky str., 54-275', 364),
        ('Minsk', 'Bogdanovicha str., 89-2H', 369),
        ('Shklov', 'Fabrichnaya str., 26A', 371),
        ('Borisov', ' Chapaev str., 27-43', 372),
        ('Gomel', 'Sukhoi str., 1B', 374),
        ('Pruzhany', ' lane. Aptekarsky, 4B', 376),
        ('Molodechno', 'ul. Volynets, 9-23', 377),
        ('Rogachev', 'Lenin str., 41-15', 380),
        ('Minsk', 'Rotmistrova str., 42', 382),
        ('Novopolotsk', 'Molodezhnaya str., 134-178', 384),
        ('Minsk', 'Romanovskaya Sloboda str., 13-5H', 385),
        ('Rechitsa', 'Grigory Shirma str., 30', 389),
        ('Brest', 'Volgogradskaya str., 4A-1', 390),
        ('Volkovysk', 'Lenin str., 57', 392),
        ('Gomel', 'ave. October, 2B', 393),
        ('Uzda', 'K.Marx Street, 90/2', 396),
        ('Minsk', 'Nikola Tesla Street, 6-1', 398),
        ('Pinsk', ' ave. Zholtovsky, 10-34', 399),
        ('Minsk', 'Nalibokskaya str., 12', 401),
        ('Gomel', 'Ilyich str., 333', 402),
        ('Bobruisk', 'Baharova str., 31', 405),
        ('Krichev', ' mkr. Sozh, 11', 406),
        ('Myadel', 'N.K. Krupskaya str., 5', 408),
        ('Borisov', 'Trusova str., 32-2', 412),
        ('Mozyr', 'b-R. Youth, 59A. Boulevard shopping Center', 413),
        ('Columns', 'Leninskaya str., 91', 415),
        ('Brest', 'Makhnovich str., 35-88', 416),
        ('Lyakhovichi', 'September 17 str., 7', 419),
        ('Baranovichi', 'ul. Voikova, 14-13', 420),
        ('Klimovichi', 'ul. Sovetskaya, 65A', 421),
        ('Grodno', 'Viktor Sayapin str., 10-84', 422),
        ('Maryina Gorka', 'Leninskaya str., 63-3', 433),
        ('Dokshitsy', 'Pionerskaya str., 18-2', 437),
        ('Shchuchin', 'ul. Lenin, 36-4', 439),
        ('Svetlogorsk', 'Sportivnaya str., 11/1-1', 442),
        (' Minsk', ' Kalinovskiy str., 101', 443),
        ('Baranovichi', 'F.Skaryna str., 17A', 444),
        ('Grodno', ' Suvorov str., 298', 445),
        ('Kobrin', 'Pushkin str., 14-89 (m-n "Euroopt)', 448),
        ('Grodno', ' Dzerzhinskiy str., 101-3', 453),
        ('Baran', 'Orshanskaya str., 26a', 454),
        ('Novolukoml', 'Kommunalnaya str., 1', 456),
        ('Dobrush', 'Knyaz Paskevich str., 13-49', 459),
        ('Svetlogorsk', 'Azalova str., in the area of house No. 61', 463),
        ('Stolin', 'Bykovsky str., 29/1', 465),
        ('Gorodok', '87-1 K.Marx Street', 467),
        ('Machulishchi', ' Molodezhnaya str., 39', 469),
        ('Minsk', 'Yesenina str., 30 room 2H', 470),
        ('Soligorsk', 'Molodezhnaya str., 6', 471),
        ('Vitebsk', 'Gorovets str., 8a', 472),
        ('Orsha', ' Vladimir Lenin str., 25-57', 473),
        ('Gomel', 'Sviridov str., 13',474),
        ('Malorita', 'Lermontov str., 4', 478),
        ('Polotsk', 'Shenyagin str., 54', 481),
        ('Lida', ' Varshavskaya str., 58, room 2', 483),
        ('Minsk', ' Oleg Koshevoy str., 8-2', 484),
        ('Soligorsk', ' ul. Oktyabrskaya, 27a',485),
        ('Volozhin', ' pl. Freedom, 5', 487),
        ('Mogilev', 'Gomelskoe sh., 55/1', 488),
        ('Lida', 'Kachana str., 29', 491),
        ('Mozyr', 'Malinina str., 1a', 492),
        ('Minsk', 'Malinina str., 24', 494),
        ('Mogilev', 'Yakubovsky str., 51B', 495),
        ('Tolochin', 'Lenin str., 53a', 496),
        ('Brest', 'Pisatel Smirnov str., 19A-62', 497),
        ('Minsk', 'Varvasheni str., 16-1', 501),
        ('Kletsk', 'Pervomayskaya str., 6', 503),
        ('Vitebsk', ' ave. Builders, 1', 506),
        ('Minsk', ' Knyagininskaya str., 10-66', 507),
        ('Vitebsk', ' Budennogo str., 7', 508),
        ('Gomel', 'Katunina str., 5-46', 510),
        ('Baranovichi', 'Kabushkina str., 108', 512),
        ('Old Roads', 'Sverdlov str., 39', 513),
        ('Minsk', 'Sukharevskaya str., 62', 514),
        ('Minsk', 'Biryuzova str., 11', 515),
        ('Minsk', 'Kamennogorskaya str., 66', 516),
        ('Slutsk', 'Maxim Bogdanovich str., 21', 518),
        ('Minsk', 'Kiselyov str., 17-56', 519),
        ('Kostyukovichi', ' Molodezhny Microdistrict, 13', 520),
        ('Minsk', 'Gamarnik str., 30 room 271', 522),
        ('Postavy', '17 September str., 1-6', 523),
        ('Gomel', '6-1 Vladimirova str.', 524),
        ('Mogilev', 'Grunvaldskaya str., 26-466', 525),
        ('Belynichi', 'Kalinina str., 40', 526),
        ('Krupki', ' Kirova str., 7/1', 527),
        ('Minsk', 'Grekova str., 4-92', 528),
        ('Zaslavl', 'ul. Sovetskaya, 112/1', 531),
        ('Minsk', ' Kolesnikova str., P.R., 20-135', 532),
        ('Grodno', ' 5a Vrublevsky str.', 533),
        ('Birch', 'ul. Oktyabrskaya, 27-3', 534),
        ('Minsk', 'Mikhail Lynkova str. 17-1N', 536),
        ('Minsk', 'MKAD str., 301-1, administrative and commercial premises No. 1-6', 537),
        ('Vitebsk', '1st Proletarskaya str., 10', 538), 
        ('Dzerzhinsk', '4A Sharko str.', 539),
        ('Baranovichi', '50-5 Komsomolskaya str.', 540),
        ('Minsk district', ' Senitsky village, 84, district d. Senica-Kopievichi', 542),
        ('Gomel', '93B Sviridova str.', 545),
        ('Minsk', '40 Plekhanov str., room 1H', 546),
        ('Radoshkovichi', 'ul. Proletarskaya, 2A', 547),
        ('Minsk', 'Franziska Skaryna str., 5-438', 548),
        ('Borovlyany', 'Birch Grove str., 108-47', 549),
        ('Birch', 'Komsomolskaya, 3B-1', 550),
        ('Galevo', ' Pervomaiskaya str., 176A/2 (Pinsk)', 551),
        ('Grodno', '91 Maxim Gorky str. (Korona market, hall D-13).', 552),
        ('Zhlobin', 'Petrovsky str., 27A', 553),
        ('Minsk', 'ave. Independence, 168/1-3H', 554),
        ('Minsk', ' Narodnaya str., 31-1N', 556),
        ('Zhodino', 'ave. Lenin, 21/2-8j', 557),
        ('Mikashevichi', 'Pervomaiskaya str., 14-37', 558),
        ('Grodno', 'Shchors str., 11B-3', 666),
        ('Grodno', 'Kupala str., 87 (Trinity Shopping Center, 3 floor)', 777),
        ('Pinsk', ' 32 K. Marx street', 888),
        ]
        for data in point_data:
            point = Point(
                city=data[0],
                street=data[1],
                number = data[2]
            )
            db.session.add(point)
    from sqlalchemy import desc
    tovar_list = Tovar.query.order_by(desc(Tovar.status)).all()
    db.session.commit()
    if current_user.is_authenticated:
        items_cart = get_items_cart()
        return render_template('catalog.html', 
                           tovar_list=tovar_list, 
                           user=current_user,
                           items_cart=items_cart)
    else:
        return render_template('catalog.html', 
                            tovar_list=tovar_list, 
                            user=current_user)

@views.route('/login')
def login():
    if current_user.is_authenticated:
        logout_user()
    return render_template('login.html', user=current_user)

@views.route('/product/<name>')
def product(name):
    tovar = Tovar.query.filter_by(name=name).first()
    comment = Comment.query.filter_by(tovar_id=tovar.id).order_by(Comment.id.desc()).limit(5).all()  
    for com in comment:
        com.created_at = com.created_at.date()
    if tovar is None:
        return render_template('error.html'), 404
    if current_user.is_authenticated:
        items_cart = get_items_cart()
        return render_template('product.html', 
                            tovar=tovar, 
                            user=current_user, 
                            comment=comment,
                            items_cart=items_cart)
    else:
        return render_template('product.html', 
                            tovar=tovar, 
                            user=current_user, 
                            comment=comment)

@views.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html', 
                           user=current_user)
    
@views.route('/account')
@login_required
def account():
    items_cart = get_items_cart()
    message = Message.query.filter_by(user_email=current_user.email).order_by(Message.created_at.desc()).all()
    for mes in message:
        mes.created_at = mes.created_at.strftime('%Y-%m-%d %H:%M')
    return render_template('account.html', 
                           message=message,
                           user=current_user,
                           items_cart=items_cart)
    
@views.route('/profile/common')
@login_required
def profile_common():
    items_cart = get_items_cart()
    return render_template('profile_common.html', 
                           user=current_user,
                           items_cart=items_cart)

@views.route('/profile/password')
@login_required
def profile_password():
    items_cart = get_items_cart()
    return render_template('profile_password.html', 
                           user=current_user, 
                           items_cart=items_cart)

@views.route('/profile/orders')
@login_required
def profile_orders():
    items_cart = get_items_cart()
    orders = Order.query.filter_by(email=current_user.email).order_by(Order.created_at.desc()).all()
    order_dict = defaultdict(list)
    status = {}
    adress = {}
    city = {}
    country = {}
    type = {}
    street = {}
    house = {}
    flat = {}
    receiving_point = {}
    fio = {}
    track_number = {}
    order_totals = {} 
    order_del = 0
    if orders:
        for order in orders:
            order_dict[order.nomerzakaza].append(order)
            if order.nomerzakaza not in order_totals:
                order_totals[order.nomerzakaza] = 0
            order_totals[order.nomerzakaza] += order.price
            first_order = Order.query.filter_by(nomerzakaza=order.nomerzakaza).first()
            status[order.nomerzakaza] = first_order.status
            city[order.nomerzakaza] = first_order.city
            country[order.nomerzakaza] = first_order.country
            type[order.nomerzakaza] = first_order.type
            street[order.nomerzakaza] = first_order.street
            house[order.nomerzakaza] = first_order.house
            flat[order.nomerzakaza] = first_order.flat
            fio[order.nomerzakaza] = first_order.fio
            track_number[order.nomerzakaza] = first_order.track_number    
            receiving_point[order.nomerzakaza] = Point.query.filter_by(id=first_order.receiving_point).first() 
            if type[order.nomerzakaza] == 'Delivery across the RB to the branch (Evropochta)':
                order_del = 2.5
            elif type[order.nomerzakaza] == 'Door-to-door delivery in the RB (Evropochta)':
                order_del = 4.5
            elif type[order.nomerzakaza] == 'Worldwide shipping':
                order_del = 7.5  
            else:
                order_del = 0
            tovar_data = Tovar.query.all()
            orders_data = Order.query.all()
            cart_data = Cart.query.all()
            sklads_data = Sklad.query.all()
            users_data = User.query.all()
        return render_template('profile_orders.html', 
                                track_number=track_number,
                                order_del=order_del,
                                adress=adress,
                                fio=fio,
                                city = city,
                                users_data=users_data,
                                sklads_data=sklads_data,
                                orders_data=orders_data, 
                                cart_data=cart_data,
                                tovar_data=tovar_data,
                                status=status,
                                country=country,
                                type = type,
                                street=street, 
                                house=house, 
                                flat=flat,
                                order_totals=order_totals,
                                receiving_point=receiving_point,
                                order_dict=order_dict, 
                                user=current_user,
                                items_cart=items_cart)  
    else:    
        return render_template('profile_orders.html', 
                                user=current_user,
                                items_cart=items_cart)  
    
@views.route('/profile/ordarea')
def ordarea():
    items_cart = get_items_cart()
    return render_template('ordarea.html', user=current_user, items_cart=items_cart)  
    
@views.route('/cart')
@login_required
def cart():
    items_cart = get_items_cart()
    point = Point.query.filter_by().all()
    items = Cart.query.filter_by(user_email=current_user.email).all()
    tovar = Tovar.query.filter_by().all()
    all_cart_price = round(sum(item.price for item in items), 2)
    items_count = Cart.query.filter_by(user_email=current_user.email).count()
    ttam_dbE = round(all_cart_price + 2.5, 2)
    ttam_ddE = round(all_cart_price + 4.5, 2)
    ttam_wws = round(all_cart_price + 7.5, 2)
    return render_template('cart.html', 
                           tovar=tovar,
                           items_count=items_count,
                           point=point,
                           items=items, 
                           user=current_user, 
                           all_cart_price=all_cart_price,
                           ttam_dbE=ttam_dbE,
                           ttam_ddE=ttam_ddE,
                           ttam_wws=ttam_wws,
                           items_cart=items_cart,
                           )

@views.route('/remove_item', methods=['POST'])
@login_required
def remove_item():
    data = json.loads(request.data)
    id = data['id']
    item = Cart.query.get(id)
    if item:
        if item.user_email == current_user.email:
            db.session.delete(item)
            db.session.commit()
    return render_template('cart.html', user=current_user)

@views.route('/faq')
def faq():
    if current_user.is_authenticated:
        items_cart = get_items_cart()
        return render_template('FAQ.html', user=current_user, items_cart=items_cart)
    else:
        return render_template('FAQ.html', user=current_user)

@views.route('/info')
def info():
    if current_user.is_authenticated:
        items_cart = get_items_cart()
        return render_template('info.html', user=current_user, items_cart=items_cart)
    else:
        return render_template('info.html', user=current_user)

@views.route('/privacy')
def privacy():
    if current_user.is_authenticated:
        items_cart = get_items_cart()
        return render_template('privacy.html', user=current_user, items_cart=items_cart)
    else:
        return render_template('privacy.html', user=current_user)
    
@views.route('/offer')
def offer():
    if current_user.is_authenticated:
        items_cart = get_items_cart()
        return render_template('offer.html', user=current_user, items_cart=items_cart)
    else:
        return render_template('offer.html', user=current_user)

@views.route('/track')
def track():
    if current_user.is_authenticated:
        items_cart = get_items_cart()
        return render_template('track.html', user=current_user, items_cart=items_cart)
    else:
        return render_template('track.html', user=current_user)

# @views.route('/map', methods=['GET', 'POST'])
# @login_required
# def map():
#     orders = Order.query.filter_by().first()
#     if not orders: 
#         flash('No active orders')
#         return render_template('catalog.html', user=current_user)
#     else:
#         with open("api.txt", "r") as api_file:
#             api_key = api_file.read().strip()
#         maps_client = googlemaps.Client(key=api_key)
#         order = None
#         if request.method == 'POST':
#             nomerzakaza = request.form.get('nomerzakaza')
#             order = Order.query.filter_by(nomerzakaza=nomerzakaza).first()
#         else:
#             order = Order.query.first()
#         A = "Налибокская 14, Минск"
#         A1 = "Nalibokskaya 14, Minsk"
#         if order:
#             if order.type == 'Delivery across the RB to the branch (Evropochta)':
#                 B = f"Налибокская 18"     
#             elif order.type == 'Door-to-door delivery in the RB (Evropochta)':
#                 B = f"{order.receiving_point}"     
#             elif order.type == 'Worldwide shipping':
#                 B = f"{order.street} {order.house}, {order.city}" 
#             geocode_resstrt1 = maps_client.geocode(A)
#             geocode_resstrt2 = maps_client.geocode(B)
#             if geocode_resstrt1 and geocode_resstrt2:
#                 lat1, lng1 = geocode_resstrt1[0]['geometry']['location']['lat'], geocode_resstrt1[0]['geometry']['location']['lng']
#                 lat2, lng2 = geocode_resstrt2[0]['geometry']['location']['lat'], geocode_resstrt2[0]['geometry']['location']['lng']
#                 origin = {'lat': lat1, 'lng': lng1}
#                 destination = {'lat': lat2, 'lng': lng2}
#                 driving_directions = maps_client.directions(A, B, mode="driving")
#                 walking_directions = maps_client.directions(A, B, mode="walking")
#                 bicycling_directions = maps_client.directions(A, B, mode="bicycling")
#                 transit_directions = maps_client.directions(A, B, mode="transit")
#                 driving_distance = driving_directions[0]['legs'][0]['distance']['text'] if driving_directions else "-"
#                 walking_distance = walking_directions[0]['legs'][0]['distance']['text'] if walking_directions else "-"
#                 bicycling_distance = bicycling_directions[0]['legs'][0]['distance']['text'] if bicycling_directions else "-"
#                 transit_distance = transit_directions[0]['legs'][0]['distance']['text'] if transit_directions else "-"
#                 HrsMinsDurationDriving = driving_directions[0]['legs'][0]['duration']['text'] if driving_directions else "-"
#                 HrsMinsDurationWalking = walking_directions[0]['legs'][0]['duration']['text'] if walking_directions else "-"
#                 HrsMinsDurationBicycling = bicycling_directions[0]['legs'][0]['duration']['text'] if bicycling_directions else "-"
#                 HrsMinsDurationTransit = transit_directions[0]['legs'][0]['duration']['text'] if transit_directions else "-"
#                 return render_template('karta.html',
#                                     order=order,
#                                     user=current_user,
#                                     api_key=api_key,
#                                     origin=origin,
#                                     destination=destination,
#                                     A1=A1,
#                                     A=A,
#                                     B=B,
#                                     driving_distance=driving_distance,
#                                     walking_distance=walking_distance,
#                                     bicycling_distance=bicycling_distance,
#                                     transit_distance=transit_distance,
#                                     HrsMinsDurationDriving=HrsMinsDurationDriving,
#                                     HrsMinsDurationWalking=HrsMinsDurationWalking,
#                                     HrsMinsDurationBicycling=HrsMinsDurationBicycling,
#                                     HrsMinsDurationTransit=HrsMinsDurationTransit)
#             else:
#                 flash('geocode_resstrt1 and geocode_resstrt2')
#                 return redirect(url_for('views.map'))
#         else:
#             flash('Some trubles')
#             return redirect(url_for('views.map'))

class MyMainView(AdminIndexView):
    @expose('/')
    def admin_stats(self):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__name__), 'website'))
        image_folder = os.path.join(base_path, 'static', 'img')
        images = [url_for('static', filename=f'img/{image}') for image in os.listdir(image_folder)]
        num_images = len(images)
        user_data = User.query.count()
        comment_data = Comment.query.count()
        sklad_data = Sklad.query.count()
        tovar_data = Tovar.query.count()
        cart_data = Cart.query.count()
        order_data = db.session.query(func.count(Order.nomerzakaza.distinct())).scalar()
        point_data = Point.query.count()
        message_data = Message.query.count()
        return self.render('admin/stats.html', 
                           user_data=user_data,
                           comment_data=comment_data,
                           sklad_data=sklad_data,
                           tovar_data=tovar_data,
                           cart_data=cart_data,
                           order_data=order_data,
                           point_data=point_data,
                           message_data=message_data,
                           images=images, 
                           num_images=num_images
                           )