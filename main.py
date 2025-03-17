# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
import random

# دالة للتحقق من إذا كان الرقم أوليًا
def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True

# دالة للتحقق من إذا كان الرقم مضاعفًا لرقم معين
def is_multiple(number, multiple):
    return number % multiple == 0

# واجهة اللعبة
class GuessNumberGame(BoxLayout):
    def __init__(self, **kwargs):
        super(GuessNumberGame, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10

        # تعليمات اللعبة
        self.label_instruction = Label(text="أدخل تخمينك (بين 1 و 25):", font_size=24, halign="right")
        self.add_widget(self.label_instruction)

        # حقل إدخال التخمين
        self.entry_guess = TextInput(multiline=False, font_size=24, halign="right")
        self.add_widget(self.entry_guess)

        # زر التخمين
        self.button_guess = Button(text="تخمين", font_size=24, background_color=(0.3, 0.7, 0.3, 1))
        self.button_guess.bind(on_press=self.check_guess)
        self.add_widget(self.button_guess)

        # نتيجة التخمين
        self.label_result = Label(text="", font_size=24, halign="right")
        self.add_widget(self.label_result)

        # زر إعادة التشغيل
        self.button_restart = Button(text="إعادة التشغيل", font_size=24, background_color=(0, 0.5, 0.8, 1))
        self.button_restart.bind(on_press=self.restart_game)
        self.add_widget(self.button_restart)

        # بدء اللعبة
        self.restart_game()

    # بدء اللعبة
    def restart_game(self, *args):
        self.secret_number = random.randint(1, 25)
        self.attempts = 0
        self.label_result.text = "مرحبًا! لقد اخترت رقمًا بين 1 و 25. هل يمكنك تخمينه؟"
        self.entry_guess.text = ""

    # التحقق من التخمين
    def check_guess(self, *args):
        guess = self.entry_guess.text

        if not guess.isdigit():
            self.show_popup("خطأ", "من فضلك أدخل رقمًا صحيحًا!")
            return

        guess = int(guess)
        self.attempts += 1

        if guess < self.secret_number:
            self.label_result.text = "الرقم الذي تخمنه أقل من الرقم الصحيح. حاول مرة أخرى!"
        elif guess > self.secret_number:
            self.label_result.text = "الرقم الذي تخمنه أعلى من الرقم الصحيح. حاول مرة أخرى!"
        else:
            self.show_popup("مبروك!", f"لقد خمنت الرقم الصحيح ({self.secret_number}) في {self.attempts} محاولة!")
            self.restart_game()
            return

        # إعطاء تلميحات إضافية
        if self.attempts == 2:
            if self.secret_number > 10:
                self.label_result.text = "تلميح: الرقم الصحيح أكبر من 10."
            else:
                self.label_result.text = "تلميح: الرقم الصحيح أقل من أو يساوي 10."
        elif self.attempts == 3:
            if self.secret_number % 2 == 0:
                self.label_result.text = "تلميح: الرقم الصحيح هو رقم زوجي."
            else:
                self.label_result.text = "تلميح: الرقم الصحيح هو رقم فردي."
        elif self.attempts == 5:
            if is_prime(self.secret_number):
                self.label_result.text = "تلميح: الرقم الصحيح هو رقم أولي."
            else:
                self.label_result.text = "تلميح: الرقم الصحيح هو رقم غير أولي."
        elif self.attempts == 7:
            if is_multiple(self.secret_number, 3):
                self.label_result.text = "تلميح: الرقم الصحيح مضاعف للرقم 3."
            elif is_multiple(self.secret_number, 5):
                self.label_result.text = "تلميح: الرقم الصحيح مضاعف للرقم 5."
            else:
                self.label_result.text = "تلميح: الرقم الصحيح ليس مضاعفًا لـ 3 أو 5."
        elif self.attempts == 9:
            if self.secret_number > 15:
                self.label_result.text = "تلميح: الرقم الصحيح أكبر من 15."
            else:
                self.label_result.text = "تلميح: الرقم الصحيح أقل من أو يساوي 15."

        # إذا انتهت المحاولات
        if self.attempts >= 10:
            self.show_popup("خسرت!", f"للأسف، لقد خسرت! الرقم الصحيح كان: {self.secret_number}.")
            self.restart_game()

    # عرض نافذة منبثقة
    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message, font_size=24), size_hint=(0.8, 0.4))
        popup.open()

# تطبيق Kivy
class GuessNumberApp(App):
    def build(self):
        Window.clearcolor = (0.94, 0.94, 0.94, 1)  # لون الخلفية
        return GuessNumberGame()

# تشغيل التطبيق
if __name__ == "__main__":
    GuessNumberApp().run()
