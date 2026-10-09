from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Applicant:
    """Соискатель и его профессиональный профиль."""
    applicant_id: int
    full_name: str
    profession: str
    skills: List[str] = field(default_factory=list)
    experience_years: int = 0
    contact: str = ""

    def matches(self, vacancy: "Vacancy") -> bool:
        """Возвращает True, если профессия совпадает и хватает опыта."""
        return (self.profession.casefold() == vacancy.profession.casefold()
                and self.experience_years >= vacancy.min_experience)


@dataclass
class Employer:
    """Работодатель, публикующий вакансии."""
    employer_id: int
    name: str
    contact: str


@dataclass
class Vacancy:
    """Открытая позиция работодателя."""
    vacancy_id: int
    employer_id: int
    title: str
    profession: str
    min_experience: int
    salary: int
    active: bool = True


@dataclass
class Selection:
    """Результат подбора конкретного соискателя на вакансию."""
    applicant_id: int
    vacancy_id: int
    status: str = "Предложена"


class RecruitmentAgency:
    """Координирует справочники и бизнес-операции агентства."""
    def __init__(self):
        self.applicants: List[Applicant] = []
        self.employers: List[Employer] = []
        self.vacancies: List[Vacancy] = []
        self.selections: List[Selection] = []

    def add_applicant(self, applicant: Applicant) -> None:
        if any(x.applicant_id == applicant.applicant_id for x in self.applicants):
            raise ValueError("Соискатель с таким ID уже существует")
        self.applicants.append(applicant)

    def add_employer(self, employer: Employer) -> None:
        if any(x.employer_id == employer.employer_id for x in self.employers):
            raise ValueError("Работодатель с таким ID уже существует")
        self.employers.append(employer)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        if not any(x.employer_id == vacancy.employer_id for x in self.employers):
            raise ValueError("Сначала добавьте работодателя")
        if any(x.vacancy_id == vacancy.vacancy_id for x in self.vacancies):
            raise ValueError("Вакансия с таким ID уже существует")
        self.vacancies.append(vacancy)

    def find_matches(self, applicant_id: int) -> List[Vacancy]:
        applicant = next((x for x in self.applicants if x.applicant_id == applicant_id), None)
        if applicant is None:
            raise ValueError("Соискатель не найден")
        return [v for v in self.vacancies if v.active and applicant.matches(v)]

    def create_selection(self, applicant_id: int, vacancy_id: int) -> Selection:
        if not any(v.vacancy_id == vacancy_id for v in self.find_matches(applicant_id)):
            raise ValueError("Эта вакансия не подходит соискателю или закрыта")
        selection = Selection(applicant_id, vacancy_id)
        self.selections.append(selection)
        return selection

    def seed_demo_data(self) -> None:
        """Добавляет демонстрационные данные для первого запуска."""
        self.add_employer(Employer(1, "ООО Альфа", "+7 900 000-00-01"))
        self.add_employer(Employer(2, "АО Вектор", "+7 900 000-00-02"))
        self.add_applicant(Applicant(1, "Анна Смирнова", "Python-разработчик",
                                     ["Python", "Django"], 2, "anna@example.com"))
        self.add_applicant(Applicant(2, "Илья Петров", "Аналитик данных",
                                     ["SQL", "Excel"], 1, "ilya@example.com"))
        self.add_vacancy(Vacancy(1, 1, "Python-разработчик", "Python-разработчик", 1, 120000))
        self.add_vacancy(Vacancy(2, 2, "Младший аналитик", "Аналитик данных", 0, 90000))


def show_applicants(agency: RecruitmentAgency) -> None:
    print("\nСоискатели:")
    for a in agency.applicants:
        print(f"{a.applicant_id}. {a.full_name} — {a.profession}, опыт: {a.experience_years} лет")


def show_vacancies(agency: RecruitmentAgency) -> None:
    print("\nВакансии:")
    for v in agency.vacancies:
        if v.active:
            employer = next(e.name for e in agency.employers if e.employer_id == v.employer_id)
            print(f"{v.vacancy_id}. {v.title} — {employer}; от {v.salary} руб.")


def main() -> None:
    agency = RecruitmentAgency()
    agency.seed_demo_data()
    print("АС кадрового агентства. Демонстрационный режим.")
    while True:
        print("\n1 — список соискателей\n2 — список вакансий\n3 — подбор вакансий"
              "\n4 — зарегистрировать подходящий подбор\n0 — выход")
        command = input("Ваш выбор: ").strip()
        try:
            if command == "1":
                show_applicants(agency)
            elif command == "2":
                show_vacancies(agency)
            elif command == "3":
                applicant_id = int(input("ID соискателя (1 или 2): "))
                matches = agency.find_matches(applicant_id)
                print("Подходящие вакансии:" if matches else "Подходящих вакансий нет.")
                for vacancy in matches:
                    print(f"{vacancy.vacancy_id}. {vacancy.title}, зарплата от {vacancy.salary} руб.")
            elif command == "4":
                applicant_id = int(input("ID соискателя: "))
                vacancy_id = int(input("ID вакансии: "))
                selection = agency.create_selection(applicant_id, vacancy_id)
                print(f"Подбор зарегистрирован: статус «{selection.status}».")
            elif command == "0":
                print("Работа программы завершена.")
                break
            else:
                print("Выберите пункт из меню.")
        except ValueError as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
