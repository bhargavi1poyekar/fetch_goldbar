from goldbar import GoldBarWeighing

if __name__ == "__main__":

    # Context Management
    with GoldBarWeighing() as gb:
        # Reset if any of the bowl value is set.
        gb.reset()
        fake_bar = gb.find_fake_bar()
        print(f"\nFake bar is: {fake_bar}")
        gb.validate_answer(fake_bar)
        gb.print_weighings_list()
    