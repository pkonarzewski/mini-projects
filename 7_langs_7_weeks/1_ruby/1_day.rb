properties = ['object oriented' , 'duck typed' , 'productive' , 'fun' ]
properties.each { |property| puts "Ruby is #{property}"}

4
4.class
4.methods

x = 4
x < 5
false
true


puts 'This appears to be false.' unless x == 4
puts 'This appears to be true.' if x == 4

if x == 4
    puts 'This appears to be true.'
end

unless x == 4
    puts 'This appeasr to be false.'
else
    puts 'This true'
end

puts 'This ap true' if not true
puts 'This appease to be true.' if !true


x = x + 1 while x < 10
puts x

x = x - 1 until x == 0
puts x

while x < 10
    x = x + 1
    puts x
end

# everything except nil and false evaluate to true
puts 'true: 0' if 0
puts 'true: 1' if 1
puts 'true: nil' if nil
puts 'true: false' if false

puts '==Equality'
puts (true and false)
puts (true or false)
puts (false && false)
puts (true | false)

# full conditions: &, |
# shortcircuts conditions: &&, ||
# false && this_is_error

# true || this_wont_cause_error
# true | this_is_error

# typing
# 4 + 'four' error!

def add_them_up
    4 + 'four'
end

def add_them_up_corr(num)
    4 + num
end

puts 'Duck typing'
i = 0
a = ['100', 100.0]
while i < 2
    puts a[i].to_i
    i = i + 1
end
# Duck typing doesn’t care what the underlying type might be. If it walks like a duck and quacks
# like a duck, it’s a duck. In this case, the quack method is to_i.

# convention about parethesis
# all are ok
# simillar to Python2 print
puts add_them_up_corr 1
puts add_them_up_corr(1)
puts(add_them_up_corr 1)
puts(add_them_up_corr(1))



# Find

# replace str
sentence = 'test me'
puts sentence
puts(sentence.sub('me', 'you'))

# Regexp
puts /stack/ =~ 'haystack'  # index where begins pattern
puts /y/.match('haystack')
puts /needle/.match('haystack')  # nil returned

line = 'Many languages exmpl Perl'
if line =~ /Perl|Python/
  puts "Scripting language mentioned: #{line}"
end

# Ranges
puts (-1..5).to_a
puts ('a'..'e').to_a

# HOME WORK
puts "==============================\nHOME WORK\n\n"

puts 'Hello, world'

puts /Ruby/ =~ 'Hello, Ruby.'

x = 0
while x < 10
    x = x + 1
    puts "#{x} Patryk"
end

puts "============================\nLETS PLAY GAME"

# Simple version
# q_number = rand(1)
# q = gets.to_i until q == q_number
# puts "Grats, number was #{q_number} "

# Full version with hints
q_number = rand(10)
q = -1

while q_number != q
    q = gets.to_i

    if q > q_number
        puts 'to big'
    elsif q < q_number
        puts 'to small'
    else
        puts "Grats, number was #{q_number}"
    end
end
