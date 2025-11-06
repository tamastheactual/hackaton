    auto luckiest = std::ranges::max_element(passengers, {}, [](auto& passenger)
        {
            auto lower_limit = std::make_tuple(passenger.birth_date.year - 2, passenger.birth_date.month, passenger.birth_date.day);
            auto upper_limit = std::make_tuple(passenger.birth_date.year + 2, passenger.birth_date.month, passenger.birth_date.day);
            return std::ranges::count_if(passengers | std::views::transform([](auto& p) { return std::make_tuple(p.birth_date.year, p.birth_date.month, p.birth_date.day); }),
                [&](auto date)
                {
                    return date >= lower_limit && date <= upper_limit;
                });
        });
    std::print("A legszerencsesebb utas: {}\n", luckiest->name);
