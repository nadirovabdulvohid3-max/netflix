from django.core.management.base import BaseCommand
from Movie.models import Movie, Actor

class Command(BaseCommand):
    help = "Ma'lumotlar bazasini default aktyor va kinolar bilan to'ldiradi"

    def handle(self, *args, **options):
        self.stdout.write("Bazani to'ldirish boshlandi...")

        # 1. Standart aktyorlarni yaratish (get_or_create xatolikni oldini oladi)
        actor1, _ = Actor.objects.get_or_create(id=1, name="piter", gender="male")
        actor2, _ = Actor.objects.get_or_create(id=2, name="John Doe", gender="male")
        actor3, _ = Actor.objects.get_or_create(id=3, name="Alya", gender="female")

        # 2. Standart kinolarni yaratish
        movie1, _ = Movie.objects.get_or_create(
            id=1,
            title="Spiderman",
            year=2002,
            genre="Action"
        )
        movie2, _ = Movie.objects.get_or_create(
            id=3,
            title="Avatar",
            year=2009,
            genre="Sci-Fi"
        )

        # 3. Aktyorlarni kinoga bog'lash (ManyToMany munosabati)
        movie1.actors.add(actor1)  # Spiderman'ga piter'ni qo'shish
        movie2.actors.add(actor2, actor3)

        self.stdout.write(self.style.SUCCESS("Baza muvaffaqiyatli to'ldirildi!"))