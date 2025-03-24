from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
import random

# إعدادات النافذة
Window.size = (400, 600)

# دالة للتحقق من إذا كان الرقم أوليًا
def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True

# دالة للتحقق من إذا كان الرقم مضاعفًا لرقم معين
def is_multiple(number, multiple):
    return number % multiple == 0

# واجهة المستخدم
class GuessNumberApp(App):
    def build(self):
        self.secret_number = random.randint(1, 25)
        self.attempts = 0
        self.title = "لعبة تخمين الرقم"

        # التصميم الرئيسي
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # نص التعليمات
        self.label_instruction = Label(
            text="أدخل تخمينك (بين 1 و 25):",
            font_size=24,
            color=(0, 0, 0, 1),
        )
        self.layout.add_widget(self.label_instruction)

        # حقل إدخال التخمين
        self.entry_guess = TextInput(
            font_size=24,
            multiline=False,
            input_type="number",
            hint_text="أدخل رقمًا هنا",
        )
        self.layout.add_widget(self.entry_guess)

        # زر التخمين
        self.button_guess = Button(
            text="تخمين",
            font_size=24,
            background_color=(0, 0.7, 0, 1),
            on_press=self.check_guess,
        )
        self.layout.add_widget(self.button_guess)

        # نتيجة التخمين
        self.label_result = Label(
            text="",
            font_size=20,
            color=(0, 0, 0, 1),
        )
        self.layout.add_widget(self.label_result)

        # زر إعادة التشغيل
        self.button_restart = Button(
            text="إعادة التشغيل",
            font_size=24,
            background_color=(0, 0.5, 1, 1),
            on_press=self.restart_game,
        )
        self.layout.add_widget(self.button_restart)

        return self.layout

    # دالة التحقق من التخمين
    def check_guess(self, instance):
        guess = self.entry_guess.text

        if not guess.isdigit():
            self.show_popup("خطأ", "من فضلك أدخل رقمًا صحيحًا!")
            return

        guess = int(guess)
        self.attempts += 1

        if guess < self.secret_number:
            self.label_result.text = "الرقم الذي تخمنه أقل من الرقم الصحيح. حاول مرة أخرى!"
            self.label_result.color = (1, 0, 0, 1)  # لون أحمر
        elif guess > self.secret_number:
            self.label_result.text = "الرقم الذي تخمنه أعلى من الرقم الصحيح. حاول مرة أخرى!"
            self.label_result.color = (1, 0, 0, 1)  # لون أحمر
        else:
            self.show_popup("مبروك!", f"لقد خمنت الرقم الصحيح ({self.secret_number}) في {self.attempts} محاولة!")
            self.restart_game()
            return

        # تلميحات إضافية
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

    # دالة إعادة التشغيل
    def restart_game(self, instance=None):
        self.secret_number = random.randint(1, 25)
        self.attempts = 0
        self.label_result.text = "مرحبًا! لقد اخترت رقمًا بين 1 و 25. هل يمكنك تخمينه؟"
        self.label_result.color = (0, 0, 0, 1)  # لون أسود
        self.entry_guess.text = ""

    # دالة لعرض رسائل Popup
    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        popup_label = Label(text=message, font_size=20, color=(0, 0, 0, 1))
        popup_button = Button(text="حسنًا", font_size=20, background_color=(0, 0.7, 0, 1))
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
        popup_button.bind(on_press=popup.dismiss)
        popup.open()

# تشغيل التطبيق
if __name__ == "__main__":
    GuessNumberApp().run()
